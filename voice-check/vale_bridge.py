#!/usr/bin/env python3
"""
vale_bridge.py — run Vale from writing_check.py and merge its findings into the
voicing report.

WHY THIS EXISTS
---------------
voice-check and Vale overlap on exactly one kind of check: "does this fixed
string appear." They do not overlap anywhere else, and the boundary is not
"deterministic vs. not" — it is narrower than that, and the reason matters:

    Vale rules are STATIC FILES scoped by FILE GLOB.
    voice-check thresholds are PER-GENRE and are re-derived from a corpus.

June's profile sets `hedge_max` to 0 for a tech cover letter and 4 for a
research paper; `long_sentence_words` runs 30 (social media) to 55 (research
paper). Vale cannot see which genre a document is being written in — `--genre`
is an argument to writing_check.py, not a property of the file path. So any
check with a NONZERO or GENRE-VARYING threshold has to stay on the voice-check
side, and any check whose threshold is a flat zero ("this phrase must not
appear") is expressible in Vale as an `existence` rule and belongs there.

That line, not "deterministic vs. judgment," is what this module implements:

    Vale owns   — presence of a fixed string or a fixed syntactic shape
                  (copular/cleft, nominalization, forbidden claims, hedges,
                  corporate register, padding, self-aggrandizement)
    voice-check owns — counts measured against a tunable threshold, the
                  stylometric distance from the corpus centroid, the genre
                  overlays, the learning loop, and the 54 qualitative checks
                  that are prompts for a model

CONSEQUENCE FOR MERGING
-----------------------
Because the Vale style packages were written by hand from the same profile
lexicons that writing_check.py reads, some findings arrive twice. This module
suppresses the Vale copy and keeps the native one, because the native one is
what feeds the flag arithmetic, the --json schema, and the learning loop.
Suppressions are counted and reported, never silent.

DRIFT
-----
The profile's pattern lexicons grow when June approves a learning-loop change.
The Vale rule files do not. `audit_coverage()` closes that gap empirically: it
synthesizes a probe sentence for every pattern in the profile, runs Vale over
it, and reports which profile patterns Vale does not catch. Run it after any
profile update; it is the maintenance signal for the hand-written rules.
"""

import json
import os
import re
import shutil
import subprocess
import sys

# Vale severities, ordered.
SEVERITY_ORDER = {"suggestion": 0, "warning": 1, "error": 2}

DEFAULT_TIMEOUT = 60

# Rule basenames that voice-check owns because their threshold is tunable and
# genre-varying. A Vale rule of the same name is a static approximation of a
# number that voice-check computes correctly, so its alerts are suppressed
# whenever the active threshold disagrees with the rule file's hard-coded one.
# Keyed by rule basename (the part after the dot), so it applies across style
# packages.
THRESHOLD_OWNED_BY_VOICE_CHECK = {
    "SentenceLength": "long_sentence_words",
    "EmDashInsertion": "emdash_insertion_words",
}


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def find_vale(explicit: str = None) -> str:
    """Locate the vale binary. Returns a path, or None if not installed."""
    if explicit:
        return explicit if os.path.isfile(explicit) and os.access(explicit, os.X_OK) else None
    found = shutil.which("vale")
    if found:
        return found
    # Common install locations that are not always on a non-interactive PATH.
    for candidate in (
        os.path.expanduser("~/bin/vale"),
        "/opt/homebrew/bin/vale",
        "/usr/local/bin/vale",
    ):
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def find_config(target_path: str) -> str:
    """Walk up from the target file looking for a Vale config.

    Vale itself does this, but only relative to the process CWD. writing_check.py
    is routinely run from somewhere else entirely, so we resolve the config
    against the DOCUMENT and pass it explicitly.
    """
    d = os.path.dirname(os.path.abspath(target_path))
    while True:
        for name in (".vale.ini", "_vale.ini", "vale.ini"):
            candidate = os.path.join(d, name)
            if os.path.isfile(candidate):
                return candidate
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------

def run_vale(filepath: str, vale_bin: str = None, config: str = None,
             timeout: int = DEFAULT_TIMEOUT) -> dict:
    """Run Vale over one file and return normalized alerts.

    Returns a dict:
        {"available": bool, "ran": bool, "alerts": [...],
         "config": str|None, "binary": str|None, "note": str|None}

    Never raises. Every failure path produces a `note` the report can print.
    """
    out = {"available": False, "ran": False, "alerts": [], "config": None,
           "binary": None, "note": None}

    vale_bin = find_vale(vale_bin)
    if not vale_bin:
        out["note"] = ("Vale not installed — mechanical rule checks skipped. "
                       "Install with `brew install vale`, then re-run.")
        return out
    out["available"] = True
    out["binary"] = vale_bin

    config = config or find_config(filepath)
    if not config:
        out["note"] = ("Vale is installed but no .vale.ini was found above "
                       f"{os.path.dirname(os.path.abspath(filepath)) or '.'} — "
                       "rule checks skipped.")
        return out
    out["config"] = config

    cmd = [vale_bin, "--no-exit", "--output=JSON", "--config", config,
           os.path.abspath(filepath)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        out["note"] = (
            f"Vale exceeded {timeout}s and was killed. This is almost always a "
            "catastrophic-backtracking regex in a style rule (a nested "
            "quantifier such as `(?:\\s*\\S+){11,}`), not a slow document. "
            "Bisect by disabling rules in .vale.ini until it returns."
        )
        return out
    except OSError as e:
        out["note"] = f"Vale could not be executed ({e}) — rule checks skipped."
        return out

    if not proc.stdout.strip():
        if proc.returncode != 0:
            err = (proc.stderr or "").strip().splitlines()
            out["note"] = ("Vale exited without output: "
                           + (err[0] if err else f"return code {proc.returncode}"))
            return out
        # No output and clean exit means genuinely zero alerts.
        out["ran"] = True
        return out

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        err = (proc.stderr or proc.stdout or "").strip().splitlines()
        out["note"] = ("Vale returned unparseable output: "
                       + (err[0] if err else "(empty)"))
        return out

    # Vale's JSON is {path: [alert, ...]}. Some builds emit a bare list on error.
    if isinstance(payload, dict):
        raw_alerts = []
        for _path, items in payload.items():
            if isinstance(items, list):
                raw_alerts.extend(items)
    elif isinstance(payload, list):
        raw_alerts = payload
    else:
        out["note"] = "Vale returned an unexpected JSON shape — rule checks skipped."
        return out

    alerts = []
    for a in raw_alerts:
        if not isinstance(a, dict):
            continue
        check = a.get("Check", "") or ""
        span = a.get("Span") or [0, 0]
        alerts.append({
            "check": check,
            "rule": check.split(".", 1)[1] if "." in check else check,
            "package": check.split(".", 1)[0] if "." in check else "",
            "severity": (a.get("Severity") or "suggestion").lower(),
            "line": a.get("Line", 0),
            "span": span,
            "match": a.get("Match", "") or "",
            "message": a.get("Message", "") or "",
            "link": a.get("Link", "") or "",
        })
    out["ran"] = True
    out["alerts"] = alerts
    return out


# ---------------------------------------------------------------------------
# Merge
# ---------------------------------------------------------------------------

def _native_reported_spans(results: dict) -> set:
    """(line, lowercased phrase) pairs writing_check.py already reported.

    Only the categories that were ported into Vale are collected. Long
    sentences and readability have no per-phrase representation and are handled
    by the threshold-ownership rule instead.
    """
    seen = set()
    buckets = (
        ("hedges", "word"),
        ("aggrandizing", "phrase"),
        ("padding", "phrase"),
        ("corporate_jargon", "phrase"),
        ("product_descriptions", "text"),
        ("topic_sentences", "text"),
        ("connectors", "word"),
    )
    for key, field in buckets:
        block = results.get(key) or {}
        for item in block.get("items", []) or []:
            text = (item.get(field) or "").strip().lower()
            if text:
                seen.add((item.get("line"), text))
    return seen


def merge(vale_result: dict, results: dict, active_thresholds: dict = None,
          rule_static_values: dict = None) -> dict:
    """Fold Vale alerts into the voicing results.

    Suppression happens for three reasons, each counted separately so the
    report can say what it dropped and why:

      duplicate_rule   the same span flagged by two style packages carrying the
                       same rule name (JuneBloch.SentenceLength and
                       JuneProse.SentenceLength both exist)
      native_overlap   writing_check.py already reported this phrase on this
                       line, from the profile lexicon the Vale rule was ported
                       from
      threshold_owned  a Vale rule hard-codes a number that the active genre
                       overrides; voice-check reports it correctly instead
    """
    active_thresholds = active_thresholds or {}
    rule_static_values = rule_static_values or {}

    native = _native_reported_spans(results)

    kept, suppressed = [], {"duplicate_rule": 0, "native_overlap": 0,
                            "threshold_owned": 0}
    threshold_notes = []
    seen_spans = set()

    for a in vale_result.get("alerts", []):
        rule = a["rule"]

        # 1. Threshold-bearing rules voice-check owns — always suppressed.
        #
        # When the numbers agree, the Vale hit is redundant with a section the
        # report already prints, and Vale's `Match` for an occurrence rule is
        # the first token of the sentence ("I", "Cabrillo"), which is useless to
        # read. When they disagree, the Vale hit is simply wrong for this genre.
        # Neither case is worth showing, so the rule is suppressed either way and
        # the reason is stated.
        if rule in THRESHOLD_OWNED_BY_VOICE_CHECK:
            thresh_key = THRESHOLD_OWNED_BY_VOICE_CHECK[rule]
            active = active_thresholds.get(thresh_key)
            static = rule_static_values.get(rule)
            suppressed["threshold_owned"] += 1
            if active is not None and static is not None and float(static) != float(active):
                note = (f"{rule}: Vale hard-codes {static:g}, active genre "
                        f"threshold is {active:g} — Vale's number is wrong here; "
                        f"voice-check reports it above")
            else:
                note = (f"{rule}: threshold-bearing and genre-varying — "
                        f"voice-check owns it and reports it above")
            if note not in threshold_notes:
                threshold_notes.append(note)
            continue

        # 2. Same span, same rule name, different package.
        span_key = (a["line"], tuple(a["span"]), rule)
        if span_key in seen_spans:
            suppressed["duplicate_rule"] += 1
            continue
        seen_spans.add(span_key)

        # 3. Already reported natively from the same lexicon.
        match_lc = a["match"].strip().lower()
        if match_lc and (a["line"], match_lc) in native:
            suppressed["native_overlap"] += 1
            continue

        kept.append(a)

    # Group by severity, then by check, so each rule's hits read as one block
    # instead of the same header repeating down the page.
    kept.sort(key=lambda a: (-SEVERITY_ORDER.get(a["severity"], 0), a["check"], a["line"]))

    by_severity = {"error": 0, "warning": 0, "suggestion": 0}
    for a in kept:
        if a["severity"] in by_severity:
            by_severity[a["severity"]] += 1

    return {
        "available": vale_result.get("available", False),
        "ran": vale_result.get("ran", False),
        "note": vale_result.get("note"),
        "config": vale_result.get("config"),
        "binary": vale_result.get("binary"),
        "alerts": kept,
        "counts": by_severity,
        "total": len(kept),
        "suppressed": suppressed,
        "threshold_notes": threshold_notes,
    }


def read_rule_static_values(config_path: str) -> dict:
    """Read `max:` out of occurrence rules so merge() can compare Vale's
    hard-coded number to the active threshold instead of guessing.

    Deliberately a line scan, not a YAML parse: this must not add a PyYAML
    dependency to a script whose whole point is that it runs anywhere.
    """
    values = {}
    if not config_path:
        return values
    root = os.path.dirname(os.path.abspath(config_path))
    styles_path = "styles"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().lower().startswith("stylespath"):
                    styles_path = line.split("=", 1)[1].strip()
                    break
    except OSError:
        return values

    styles_dir = os.path.join(root, styles_path)
    if not os.path.isdir(styles_dir):
        return values

    for pkg in os.listdir(styles_dir):
        pkg_dir = os.path.join(styles_dir, pkg)
        if not os.path.isdir(pkg_dir):
            continue
        for fname in os.listdir(pkg_dir):
            if not fname.endswith((".yml", ".yaml")):
                continue
            rule = os.path.splitext(fname)[0]
            try:
                with open(os.path.join(pkg_dir, fname), "r", encoding="utf-8") as f:
                    for line in f:
                        m = re.match(r"^\s*max:\s*([0-9.]+)\s*$", line)
                        if m:
                            values.setdefault(rule, float(m.group(1)))
                            break
            except OSError:
                continue
    return values


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def format_section(merged: dict, width: int = 51) -> str:
    """Render the Vale block for the text report."""
    lines = ["═" * width, "  MECHANICAL RULES (Vale)", "═" * width, ""]

    if not merged.get("ran"):
        lines.append("  " + (merged.get("note") or "Vale did not run."))
        lines.append("")
        return "\n".join(lines)

    cfg = merged.get("config")
    if cfg:
        lines.append(f"  Config: {cfg}")
    c = merged["counts"]
    lines.append(f"  Alerts: {merged['total']} "
                 f"({c['error']} error, {c['warning']} warning, {c['suggestion']} suggestion)")

    sup = merged["suppressed"]
    if any(sup.values()):
        parts = []
        if sup["native_overlap"]:
            parts.append(f"{sup['native_overlap']} already reported above")
        if sup["duplicate_rule"]:
            parts.append(f"{sup['duplicate_rule']} duplicate rule hits")
        if sup["threshold_owned"]:
            parts.append(f"{sup['threshold_owned']} threshold-owned by voice-check")
        lines.append("  Suppressed: " + ", ".join(parts))
    for note in merged.get("threshold_notes", []):
        lines.append(f"    {note}")
    lines.append("")

    if not merged["alerts"]:
        lines.append("  No mechanical rule violations.")
        lines.append("")
        return "\n".join(lines)

    current = None
    for a in merged["alerts"]:
        header = f"{a['severity'].upper()} — {a['check']}"
        if header != current:
            current = header
            lines.append(f"  {header}")
        match = a["match"].replace("\n", " ").strip()
        if len(match) > 70:
            match = match[:67] + "..."
        lines.append(f"    Line {a['line']}: \"{match}\"")
        lines.append(f"      {a['message']}")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Coverage audit — the learning-loop drift monitor
# ---------------------------------------------------------------------------

# Pattern categories in the profile that were ported into Vale rules. Categories
# absent here are voice-check-only by design and are not audited.
AUDITED_CATEGORIES = [
    "hedge_words",
    "self_aggrandizing",
    "narrative_padding",
    "corporate_jargon",
    "over_explanation",
    "wordy_phrases",
    "cognitive_science_jargon",
    "dual_meaning_terms_in_technical_descriptions",
]


def _sample_from_regex(pattern: str) -> str:
    """Synthesize the shortest string a regex would match.

    Walks the parsed pattern tree from the stdlib rather than trying to strip
    metacharacters textually, which gets `(?:a|b)` and `\\b` wrong. Returns None
    when the pattern uses a construct that cannot be sampled (lookarounds,
    backreferences).
    """
    try:
        import re._parser as sre_parse  # Python 3.11+
    except ImportError:  # pragma: no cover
        import sre_parse  # Python <= 3.10

    def walk(seq):
        out = []
        for op, arg in seq:
            name = str(op).split(".")[-1]
            if name == "LITERAL":
                out.append(chr(arg))
            elif name == "NOT_LITERAL":
                out.append("x" if chr(arg) != "x" else "y")
            elif name == "ANY":
                out.append("x")
            elif name == "AT":
                continue  # \b, ^, $ contribute nothing to the sample
            elif name == "IN":
                ch = None
                for sub_op, sub_arg in arg:
                    sub_name = str(sub_op).split(".")[-1]
                    if sub_name == "LITERAL":
                        ch = chr(sub_arg)
                        break
                    if sub_name == "RANGE":
                        ch = chr(sub_arg[0])
                        break
                    if sub_name == "CATEGORY":
                        cat = str(sub_arg).split(".")[-1]
                        ch = {"CATEGORY_DIGIT": "1", "CATEGORY_SPACE": " ",
                              "CATEGORY_WORD": "a"}.get(cat, "a")
                        break
                out.append(ch if ch is not None else "a")
            elif name in ("MAX_REPEAT", "MIN_REPEAT"):
                lo, _hi, sub = arg
                body = walk(sub)
                if body is None:
                    return None
                out.append(body * max(lo, 1))
            elif name == "SUBPATTERN":
                sub = arg[3] if len(arg) == 4 else arg[1]
                body = walk(sub)
                if body is None:
                    return None
                out.append(body)
            elif name == "BRANCH":
                _, branches = arg
                body = None
                for br in branches:
                    body = walk(br)
                    if body:
                        break
                if body is None:
                    return None
                out.append(body)
            elif name in ("ASSERT", "ASSERT_NOT", "GROUPREF", "GROUPREF_EXISTS"):
                continue
            else:
                return None
        return "".join(out)

    try:
        parsed = sre_parse.parse(pattern, re.IGNORECASE)
    except re.error:
        return None
    return walk(parsed)


def audit_coverage(profile: dict, filepath_hint: str, vale_bin: str = None,
                   config: str = None, workdir: str = None) -> dict:
    """Report which of the profile's ported lexicon entries Vale does not catch.

    Method is empirical, not textual: build one probe line per pattern, run Vale
    over the probe document, and see which lines produced no alert. Comparing
    regex sources between the profile and the rule files would be guesswork;
    running the actual linter is not.
    """
    vale_bin = find_vale(vale_bin)
    if not vale_bin:
        return {"ran": False, "note": "Vale not installed — coverage audit skipped."}
    config = config or find_config(filepath_hint)
    if not config:
        return {"ran": False, "note": "No .vale.ini found — coverage audit skipped."}

    probes = []          # (category, pattern, sample)
    unsamplable = []     # (category, pattern)
    for cat in AUDITED_CATEGORIES:
        for pat in profile.get("patterns", {}).get(cat, []) or []:
            sample = _sample_from_regex(pat)
            if not sample or not sample.strip():
                unsamplable.append((cat, pat))
                continue
            probes.append((cat, pat, sample.strip()))

    if not probes:
        return {"ran": False, "note": "No auditable patterns in profile."}

    # The probe lives in a temp directory, NOT in the project. Writing it beside
    # the config would mean a crashed run could leave a synthetic file that later
    # gets linted as if it were a draft. `--config` is passed explicitly, so
    # StylesPath still resolves against the real config and the `[*.md]` section
    # still matches on the .md extension.
    import tempfile

    body_lines = []
    for _cat, _pat, sample in probes:
        # One probe per stanza, wrapped in a plain sentence so sentence-scoped
        # rules have something to bind to. Blank lines between stanzas keep
        # paragraph-scoped rules from bleeding across probes, which puts each
        # probe on line 1 + 2*i.
        body_lines.append(f"I noted that {sample} in the report.")
    line_index = {1 + 2 * i: i for i in range(len(probes))}

    tmpdir = tempfile.mkdtemp(prefix="voicecheck_vale_probe_")
    probe_path = os.path.join(tmpdir, "probe.md")
    try:
        with open(probe_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(body_lines) + "\n")
        result = run_vale(probe_path, vale_bin=vale_bin, config=config)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    if not result.get("ran"):
        return {"ran": False, "note": result.get("note") or "Vale run failed."}

    hit_lines = {a["line"] for a in result["alerts"]}
    covered, uncovered = [], []
    for line_no, idx in line_index.items():
        cat, pat, sample = probes[idx]
        (covered if line_no in hit_lines else uncovered).append(
            {"category": cat, "pattern": pat, "sample": sample}
        )

    return {
        "ran": True,
        "config": config,
        "total": len(probes),
        "covered": len(covered),
        "uncovered": uncovered,
        "unsamplable": [{"category": c, "pattern": p} for c, p in unsamplable],
    }


def format_coverage_report(audit: dict) -> str:
    lines = ["", "═" * 51, "  VALE COVERAGE AUDIT (profile → rules)",
             "═" * 51, ""]
    if not audit.get("ran"):
        lines.append("  " + (audit.get("note") or "Audit did not run."))
        lines.append("")
        return "\n".join(lines)

    lines.append(f"  Config: {audit['config']}")
    lines.append(f"  Profile patterns probed: {audit['total']}  "
                 f"|  caught by Vale: {audit['covered']}  "
                 f"|  missed: {len(audit['uncovered'])}")
    lines.append("")
    lines.append("  A miss is not a bug. It means the profile lexicon has an entry")
    lines.append("  the hand-written Vale rules do not cover — usually because the")
    lines.append("  learning loop added it after the rules were written. Add it to")
    lines.append("  the relevant styles/*/*.yml, or leave it to voice-check knowingly.")
    lines.append("")

    if audit["uncovered"]:
        by_cat = {}
        for u in audit["uncovered"]:
            by_cat.setdefault(u["category"], []).append(u)
        for cat, items in sorted(by_cat.items()):
            lines.append(f"  {cat} ({len(items)} not covered)")
            for it in items:
                lines.append(f"    {it['pattern']}")
                lines.append(f"      probe: \"{it['sample']}\"")
            lines.append("")
    else:
        lines.append("  Every auditable profile pattern is covered by a Vale rule.")
        lines.append("")

    if audit["unsamplable"]:
        lines.append(f"  Not probeable ({len(audit['unsamplable'])}) — regexes with "
                     "lookarounds or backreferences; check these by hand:")
        for it in audit["unsamplable"]:
            lines.append(f"    [{it['category']}] {it['pattern']}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    # Smoke test: `python3 vale_bridge.py FILE` prints the merged section with
    # no native results to suppress against.
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    target = sys.argv[1]
    res = run_vale(target)
    print(format_section(merge(res, {}, {}, read_rule_static_values(res.get("config")))))
