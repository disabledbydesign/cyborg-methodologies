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
    if tok.startswith(("http://", "https://", "/printpress", "/critic-swarm", "/workshop", "/voice-check")):
        return False
    if re.match(r"^[\w.-]+\.(com|org|net|edu|io|ai)\b", tok):
        return False                    # a bare domain, not a path
    suffix = Path(tok.split(":")[0].split("#")[0]).suffix.lower()
    return suffix in PATH_EXTS or (tok.endswith("/") and "/" in tok)


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
    ap.add_argument("--root", action="append", default=[], help="extra root to scan (repeatable)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    roots = [SKILL_ROOT]
    if (SKILL_ROOT.parent / "critic-swarm").exists():
        roots = [SKILL_ROOT.parent]          # the whole skills repo
    for r in args.root:
        roots.append(Path(r).expanduser().resolve())
    # Auto-detect the workspace if it sits where the skill expects it.
    for guess in (Path.home() / "Documents/Filing/Job Search",):
        if guess.exists() and guess not in roots:
            roots.append(guess)

    if not args.quiet:
        print("check_wiring")
        for r in roots:
            print(f"  root: {r}{'' if r.exists() else '   (absent)'}")
        print()

    build_basename_index(roots)

    dead, forked, absolute, anchors, unverifiable = [], [], [], [], []
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
                verdict = resolve(tok, doc, roots)
                if verdict == "dead":
                    dead.append((doc, i, tok))
                elif verdict == "unverifiable":
                    unverifiable.append((doc, i, tok))
            for m in LINE_ANCHOR.finditer(line):
                anchors.append((doc, i, m.group(0).strip("`")))
            if ABS_HOME.search(line):
                absolute.append((doc, i))

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
        if not items:
            return
        print(f"\n{title} ({len(items)})")
        for it in items[:cap]:
            print("  " + fmt(it))
        if len(items) > cap:
            print(f"  … and {len(items) - cap} more")

    show("DEAD REFERENCES — cited path does not exist", dead,
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
    print(f"summary: {len(dead)} dead · {len(forked)} forked · "
          f"{len(absolute)} absolute-path lines · {len(anchors)} line anchors · "
          f"{len(unverifiable)} unverifiable")
    if dead or forked:
        print("FAIL — dead references and forked duplicates must be zero.")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
