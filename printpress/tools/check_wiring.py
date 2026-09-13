#!/usr/bin/env python3
"""check_wiring.py — fail loudly when the workflow's wiring rots.

Four checks, run across the skill repo and the workspace(s) that cite it:

  1. DEAD REFERENCES   a file cites a path that does not exist
  2. FORKED DUPLICATES the same filename in two places with different content
  3. ABSOLUTE PATHS    hardcoded /Users/<someone>/ — breaks if the tree moves
  4. LINE ANCHORS      `FILE.md:129` — rots silently on the next edit (warning only)

Exit 1 on any DEAD or FORKED finding. Absolute paths and line anchors warn.

Why this exists: on 2026-09-12 an audit found DRAFT_PLAN_TEMPLATE.md in five distinct
versions, VERSION_LOG_TEMPLATE.md in four, a `critical-swarm` typo that had been
pointing at nothing for weeks, and a Step 3.8 learning log cited as "create on first
review" that was never created — so that loop had never once fired. Every one of those
is mechanical and would have been caught the day it appeared.

Usage:
    python3 check_wiring.py                       # skill repo + auto-detected workspaces
    python3 check_wiring.py --root ~/some/dir     # add a root (repeatable)
    python3 check_wiring.py --quiet               # findings only
"""

from __future__ import annotations

import argparse
import os
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]

# Files that are created per-application at drafting time. Citing them is correct;
# their absence from the repo is not a defect.
RUNTIME_ARTIFACTS = {
    "POSTING.md", "APPLICATION_STRUCTURE.md", "FACT_INVENTORY.md", "DRAFT_PLAN.md",
    "COMPANY_PROFILE.md", "DEPARTMENT_PROFILE.md", "INTELLECTUAL_CONNECTIONS.md",
    "ATS_REPORT.md", "READER_TAKEAWAYS.md", "LEARNING_LOG.md", "VERSION_LOG.md",
    "APPLICATION_CHECKLIST.md", "FLAGS.md", "ASSEMBLY_MARKS.md", "DRAFT_STATE.md",
    "PROPOSITIONS.md", "COMMITMENT_MATRIX.md", "application-requirements.json",
    "PORTAL.md", "FIT_EVAL.md",
}

# Extensions worth resolving. Anything else in backticks is prose or a command.
PATH_EXTS = {".md", ".py", ".json", ".yml", ".yaml", ".html", ".sh", ".docx", ".pdf", ".ini", ".jsonl"}

SKIP_DIR_PARTS = {".git", "node_modules", "__pycache__", ".pytest_cache", "venv",
                  ".obsidian", ".venv", "raw_transcripts", "_deprecated_templates"}

BACKTICKED = re.compile(r"`([^`\n]{2,200})`")
LINE_ANCHOR = re.compile(r"`?([\w./-]+\.(?:md|py|json|yml|html))[:#](\d+)(?:-\d+)?`?")
ABS_HOME = re.compile(r"/Users/[A-Za-z0-9_.-]+/")
# "if it exists", "when one exists", "if any", "should one exist"
CONDITIONAL = re.compile(r"\b(if|when|should)\s+(it|one|they|any|present)\b[^.]{0,20}\bexists?\b"
                         r"|\bif\s+(it|one|any)\s+exists\b|\bif\s+present\b|\bif\s+any\b", re.I)


# Memory keys (`feedback_topic_sentences`, `project_wennergren_state`) and filename
# conventions quoted in prose (`_final.md`, `v1.md`) look like paths and are not.
MEMORY_KEY = re.compile(r"^(feedback|project|insight|decision)_[\w-]+\.md$")
SUFFIX_CONVENTION = re.compile(
    r"^(v\d+|vN|_\w+|\*_\w+|final_extracted|\w*_final|\w*_voicefinal|\w*_v\d+)\.md$")


def is_pathlike(tok: str) -> bool:
    tok = tok.strip()
    name = Path(tok).name
    if MEMORY_KEY.match(name) or SUFFIX_CONVENTION.match(name):
        return False
    if not tok or " " in tok.strip() and not tok.startswith(("~", "/", ".")):
        # allow spaces only in rooted paths (e.g. "Job Search/PIPELINE.md")
        if "/" not in tok:
            return False
    if any(c in tok for c in "[]<>*|$(){}"):
        return False            # placeholder or shell
    # A filename template is not a missing file. `triage_results_YYYY-MM-DD.md`
    # and `job_search_results_linkedin_YYYY-MM-DD.json` are instructions for
    # naming an output, and no such file is ever supposed to exist.
    if re.search(r"(YYYY|MM-DD|HH:MM|<date>|\bNNN\b)", tok):
        return False
    # An elided path is a human abbreviation, not an address. `.../Internal Docs/x`
    # and `critic-swarm/…/ats-compatibility.md` were written to be readable, and
    # resolving them is not possible even in principle.
    if "..." in tok or "\u2026" in tok:
        return False
    if tok.startswith(("http://", "https://", "/printpress", "/critic-swarm", "/workshop", "/voice-check")):
        return False
    # A hostname with a path after it is a URL missing its scheme, not a file.
    if re.match(r"^[\w-]+(\.[\w-]+)*\.(com|org|net|edu|gov|io|ai|co|uk|dev)\b", tok):
        return False
    suffix = Path(tok.split(":")[0].split("#")[0]).suffix.lower()
    return suffix in PATH_EXTS or (tok.endswith("/") and "/" in tok)


# ---------------------------------------------------------------------------
# THE ACTIVE READER SET vs. THE ARCHIVE.
#
# A dead reference in SKILL.md misroutes a live workflow: an agent follows it
# mid-draft and lands nowhere. A dead reference in an evidence write-up from
# August records where a file WAS when the write-up was made. The first is a
# defect; the second is history. Reporting both under one number made this check
# unusable as a gate — it failed with 86 findings, four of which were real, and a
# gate that always fails is a gate nobody reads.
#
# So only the active set blocks. Everything else is reported and does not fail.
# ---------------------------------------------------------------------------
ACTIVE_NAMES = {"SKILL.md", "PIPELINE.md", "DRAFTING_STANDARD.md",
                "CLAUDE.md", "AGENTS.md"}
ACTIVE_DIRS = {"genre_configs", "templates", "tools", "personas", "_always", "workflows"}
# Names that announce themselves as a record of one moment.
ARCHIVE_MARKERS = re.compile(
    r"(HANDOFF|FIELDNOTE|SWEEP|AUDIT|REVISION_ANALYSIS|RESEARCH_SYNTHESIS|"
    r"READING_LIST|EXTRACTION_NOTES|_\d{4}-\d{2}-\d{2}| copy)")
ARCHIVE_DIRS = {"_application_evidence", "agent_briefs", "synthesis", "outputs",
                "workflow-learning", "memos", "feedback"}


def is_active(p: Path) -> bool:
    """Does an agent follow this file's citations while drafting?"""
    if ARCHIVE_MARKERS.search(p.name):
        return False
    if any(part in ARCHIVE_DIRS for part in p.parts):
        return False
    if p.name in ACTIVE_NAMES:
        return True
    return p.parent.name in ACTIVE_DIRS


# Files whose citations we check. The drafting workflow only — sibling skills
# (c2c, archaeology, discourse-analysis) have their own wiring and their own owners.
SCAN_SUBDIRS = ("printpress", "critic-swarm")

# Per-repo by design; two repos each having a CLAUDE.md is not a fork.
# Per-skill / per-repo by design. Two skills each having a principles.md is not a fork.
NEVER_A_FORK = {"CLAUDE.md", "AGENTS.md", "README.md", "HANDOFF.md", "INSIGHTS.md",
                "SKILL.md", "SPEC.md", "principles.md", "STACK.md", "__init__.py",
                "conftest.py", "__main__.py"}


def scan_dirs(roots: list[Path]) -> list[Path]:
    out = []
    for root in roots:
        if not root.exists():
            continue
        subs = [root / s for s in SCAN_SUBDIRS if (root / s).is_dir()]
        if subs:
            out.extend(subs)          # a skills repo: only the drafting skills
        else:
            # A workspace: only the shared, wiring-relevant parts. Application folders
            # hold per-draft scratch citations that are nobody's wiring.
            out.append(root)
            for s in ("templates", "_application_evidence", "agent_briefs", "synthesis"):
                if (root / s).is_dir():
                    out.append(root / s)
    return out


def iter_docs(roots: list[Path]):
    for root in roots:
        if not root.exists():
            continue
        # Depth 1 for a bare workspace root; recursive inside skill dirs.
        recursive = root.name in SCAN_SUBDIRS or root.parent.name in SCAN_SUBDIRS \
            or root.name in ("templates", "_application_evidence", "agent_briefs", "synthesis")
        for p in (root.rglob("*") if recursive else root.iterdir()):
            if not p.is_file() or p.suffix.lower() not in {".md", ".sh"}:
                continue
            if any(part in SKIP_DIR_PARTS for part in p.parts):
                continue
            if ".bak" in p.name or ".frozen-backup" in p.name or p.name.endswith("~"):
                continue
            # Pasted prompts for other projects live here; their citations are that
            # project's wiring, not this one's.
            if p.name.startswith("claude_code_prompt_"):
                continue
            yield root, p


_BASENAME_INDEX: dict[str, list[Path]] = {}


def build_basename_index(roots: list[Path]) -> None:
    """Every real filename under the roots, so a bare `FOO.md` citation resolves."""
    _BASENAME_INDEX.clear()
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if not any(part in SKIP_DIR_PARTS for part in p.parts):
                _BASENAME_INDEX.setdefault(p.name, []).append(p)   # files and dirs


def resolve(tok: str, citing: Path, roots: list[Path]) -> str:
    """Return 'ok', 'dead', or 'unverifiable'."""
    raw = tok.split(":")[0].split("#")[0].strip().rstrip("/")
    if not raw:
        return "ok"
    if Path(raw).name in RUNTIME_ARTIFACTS:
        return "ok"
    if raw.startswith("~") or raw.startswith("/"):
        expanded = Path(raw).expanduser()
        if expanded.exists():
            return "ok"
        # Is it inside a root we can see? Then it is genuinely dead.
        for root in roots:
            try:
                rel = expanded.relative_to(root)
                return "ok" if (root / rel).exists() else "dead"
            except ValueError:
                continue
        return "unverifiable"      # outside every mounted root
    # relative: try the citing file's dir, its root, and every root
    candidates = [citing.parent / raw]
    for root in roots:
        candidates.append(root / raw)
        candidates.append(root.parent / raw)     # "Job Search/PIPELINE.md" from a sibling
    if any(c.exists() for c in candidates):
        return "ok"
    # A bare filename cited in prose ("see `CHECK_TRIAGE.md`") resolves if the file
    # exists anywhere under a root. Only the trailing segments need to match.
    parts = [seg for seg in raw.split("/") if seg not in (".", "..")]
    hits = _BASENAME_INDEX.get(parts[-1], [])
    for hit in hits:
        if len(parts) == 1 or str(hit).replace("\\", "/").endswith("/".join(parts)):
            return "ok"
    return "dead"


def md5(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()[:12]


# The intended end state for a consolidated artifact is ONE canonical copy plus redirect
# stubs at the old paths (so existing citations and old backups still lead somewhere).
# A stub is not a fork — recognising it is what makes consolidation expressible.
STUB_MARKERS = ("has moved", "canonical copy:", "moved 2026-", "lives at", "see instead")


def is_redirect_stub(p: Path) -> bool:
    try:
        if p.stat().st_size > 2500:
            return False
        head = p.read_text(errors="replace")[:600].lower()
    except OSError:
        return False
    return any(m in head for m in STUB_MARKERS)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", action="append", default=[],
                    help="scan exactly this root instead of auto-detecting (repeatable)")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--full", action="store_true", help="print every finding, not the first 25")
    args = ap.parse_args()

    # --root means "scan exactly these", not "these as well". Auto-detection is a
    # convenience for the bare interactive run; when a caller names its roots it
    # wants those and nothing else. Mixing the two silently pulled the real
    # workspace into the test suite's temporary trees, so every test saw the whole
    # of Job Search and the fixtures stopped meaning anything.
    if args.root:
        roots = [Path(r).expanduser().resolve() for r in args.root]
    else:
        roots = [SKILL_ROOT]
        if (SKILL_ROOT.parent / "critic-swarm").exists():
            roots = [SKILL_ROOT.parent]      # the whole skills repo
    # Auto-detect the workspace. PIPELINE.md and DRAFTING_STANDARD.md live in the
    # skill but address the WORKSPACE: their citations ("Emory/", "synthesis/...",
    # "_application_evidence/...") are relative to Job Search, because that is where
    # an agent stands when it reads them. Without the workspace root, ~200 correct
    # citations read as dead. JOB_SEARCH_ROOT overrides; the mnt/ guess is the
    # Cowork sandbox, where $HOME is the session, not the Mac home.
    guesses = []
    if args.root:
        guesses = []                          # explicit roots: guess nothing
    elif os.environ.get("JOB_SEARCH_ROOT"):
        guesses.append(Path(os.environ["JOB_SEARCH_ROOT"]).expanduser())
    if not args.root:
        guesses += [Path.home() / "Documents/Filing/Job Search",
                    Path.home() / "mnt/Job Search"]
    for guess in guesses:
        g = guess.resolve() if guess.exists() else guess
        if g.exists() and g not in roots:
            roots.append(g)
            break

    if not args.quiet:
        print("check_wiring")
        for r in roots:
            print(f"  root: {r}{'' if r.exists() else '   (absent)'}")
        print()

    # REFERENCE ROOTS are read for resolution but never scanned for their own
    # citations. The Rustin grants-research fork is a separate project with its own
    # owner, but printpress cites into it by design (SKILL.md quotes its
    # williams-cutting.md guards). Without this, a correct citation reads as dead;
    # with it scanned as a normal root, this check would start policing someone
    # else's documents.
    ref_roots = []
    for guess in () if args.root else (Path.home() / "Documents/Filing/Consulting/Rustin Institute/rustin-tools/grants-research",
                  Path.home() / "mnt/grants-research"):
        if guess.exists():
            ref_roots.append(guess.resolve())
            break
    if not args.quiet and ref_roots:
        for r in ref_roots:
            print(f"  reference root (resolve only): {r}")
        print()

    all_roots = roots + ref_roots
    build_basename_index(all_roots)

    dead, dead_archive, forked, absolute, anchors, unverifiable = [], [], [], [], [], []
    basenames: dict[str, list[Path]] = defaultdict(list)

    for root, doc in iter_docs(scan_dirs(roots)):
        try:
            text = doc.read_text(errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for tok in BACKTICKED.findall(line):
                if not is_pathlike(tok):
                    continue
                verdict = resolve(tok, doc, all_roots)
                # A citation the prose itself hedges is not a broken link. When a
                # genre config says `Spencer/` "(when one exists)", or CLAUDE.md says
                # navigate `graphify-out/wiki/index.md` "if it exists", the author has
                # already said the target is optional. Flagging it teaches the reader
                # to ignore the report.
                if verdict == "dead" and CONDITIONAL.search(line):
                    verdict = "conditional"
                if verdict == "dead":
                    (dead if is_active(doc) else dead_archive).append((doc, i, tok))
                elif verdict == "unverifiable":
                    unverifiable.append((doc, i, tok))
            for m in LINE_ANCHOR.finditer(line):
                anchors.append((doc, i, m.group(0).strip("`")))
            if ABS_HOME.search(line):
                absolute.append((doc, i))

    # ------------------------------------------------------------------
    # Reclassify citations to repositories that simply are not mounted.
    #
    # PIPELINE.md cites `/Users/june/Documents/GitHub/profile/JUNE_BLOCH_AGENT_BRIEFING.md`
    # in one place and the bare `JUNE_BLOCH_AGENT_BRIEFING.md` in another. The first is
    # correctly called unverifiable — it is outside every mounted root, so this checker
    # cannot see it. The second was called DEAD, which is a different and false claim:
    # it says the file is gone when it is merely elsewhere. Absence of evidence, not
    # evidence of absence.
    #
    # So: any name already seen as unverifiable teaches the checker that the name lives
    # outside. A bare citation of that same name is unverifiable too. The map builds
    # itself from the documents, so nothing has to be maintained by hand.
    # ------------------------------------------------------------------
    external_names = set()
    for _, _, tok in unverifiable:
        parts = [x for x in tok.strip("/").split("/") if x]
        if parts:
            external_names.add(parts[-1])
            for part in parts:
                if part not in ("Users", "june", "Documents", "GitHub", "Filing"):
                    external_names.add(part)
    still_dead = []
    for entry in dead:
        tok = entry[2]
        parts = [x for x in tok.strip("/").split("/") if x]
        if parts and (parts[-1] in external_names or parts[0] in external_names):
            unverifiable.append(entry)
        else:
            still_dead.append(entry)
    dead = still_dead

    # Forked duplicates: only across CANONICAL locations. Per-application artifacts
    # (APPLICATION_CHECKLIST.md in eleven app folders) are supposed to differ — that
    # is the workflow working, not drift. Canon is the skill's own files plus the
    # workspace's shared templates.
    CANON_SUBDIRS = ("", "templates", "genre_configs", "tools", "personas", "workflows",
                     "workflows/templates", "_application_evidence",
                     "printpress", "printpress/templates", "printpress/genre_configs",
                     "printpress/tools", "critic-swarm", "critic-swarm/personas")
    for root in roots:
        if not root.exists():
            continue
        for sub in CANON_SUBDIRS:
            d = root / sub if sub else root
            if not d.is_dir():
                continue
            for p in d.iterdir():          # depth 1 only — never descend into app folders
                if not p.is_file() or ".bak" in p.name or ".frozen-backup" in p.name:
                    continue
                if p.name in NEVER_A_FORK or is_redirect_stub(p):
                    continue
                if p.suffix.lower() in {".md", ".py", ".yml", ".html"}:
                    basenames[p.name].append(p.resolve())
    for name, paths in sorted(basenames.items()):
        if len(paths) < 2:
            continue
        hashes = {}
        for p in dict.fromkeys(paths):     # same inode via two mounts is not a fork

            try:
                hashes.setdefault(md5(p), []).append(p)
            except OSError:
                pass
        if len(hashes) > 1:
            forked.append((name, hashes))

    def show(title, items, fmt, cap=25):
        if args.full:
            cap = len(items)
        if not items:
            return
        print(f"\n{title} ({len(items)})")
        for it in items[:cap]:
            print("  " + fmt(it))
        if len(items) > cap:
            print(f"  … and {len(items) - cap} more")

    show("DEAD REFERENCES in the active workflow — an agent following these lands nowhere", dead,
         lambda t: f"{t[0].name}:{t[1]}  ->  {t[2]}")
    show("ROT in archived documents — records of where things were; not a failure", dead_archive,
         lambda t: f"{t[0].name}:{t[1]}  ->  {t[2]}")

    if forked:
        print(f"\nFORKED DUPLICATES — same name, different content ({len(forked)})")
        for name, hashes in forked[:15]:
            print(f"  {name}  —  {len(hashes)} distinct versions")
            for h, ps in hashes.items():
                for p in ps:
                    print(f"      {h}  {p}")

    if not args.quiet:
        show("WARN: absolute /Users/ paths — break if the tree moves", absolute,
             lambda t: f"{t[0].name}:{t[1]}", cap=15)
        show("WARN: line-number anchors — rot on the next edit", anchors,
             lambda t: f"{t[0].name}:{t[1]}  ->  {t[2]}", cap=15)
        show("INFO: unverifiable (outside every scanned root)", unverifiable,
             lambda t: f"{t[0].name}:{t[1]}  ->  {t[2]}", cap=15)

    print()
    print(f"summary: {len(dead)} dead in active workflow · {len(forked)} forked · "
          f"{len(dead_archive)} archived rot · {len(absolute)} absolute-path lines · "
          f"{len(anchors)} line anchors · {len(unverifiable)} unverifiable")
    if dead or forked:
        print("FAIL — dead references in the active workflow, and forked duplicates, must be zero.")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
