#!/usr/bin/env python3
"""check_landing.py — the last step, enforced.

`REVISION_ANALYSIS_2026-08-16_FAMSF.md` names the failure this exists to stop:

    "REVISION_ANALYSIS_2026-08-12.md proposed nine specific check amendments, each naming
     its target file. Observation: zero were made. … The pattern is one thing, at three
     scales: capture happens, landing doesn't. Material is drafted and cut before the author
     sees it. Flags are raised and never dispositioned. Amendments are proposed and never
     applied."

Rebuilding a lost profile in a safer location fixes the half where a file vanishes. It does
nothing about the half where an approved amendment is written down and never applied. This
script is that half.

Proposals in this workspace are written in a consistent shape — each names a TARGET ID and a
TARGET FILE:

    **1 · `ARG-4` · `INST` · `_application_evidence/DRAFTING_STANDARD.md`**

So landing is mechanically checkable: does that id now appear in that file? A NEW check that
is absent has provably not landed. An AMENDMENT to an existing check cannot be verified by
presence alone, so it is reported as needing human confirmation rather than silently passed.

Usage:
    python3 check_landing.py --workspace "~/Documents/Filing/Job Search"
    python3 check_landing.py --workspace ... --skill ~/.claude/skills/printpress

Exit 1 if any proposal has provably not landed.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SOURCES = ["_application_evidence/REVISION_ANALYSIS_2026-08-12.md",
           "_application_evidence/REVISION_ANALYSIS_2026-08-16_FAMSF.md",
           "_application_evidence/AUTHOR_REVISION_SPEC.md",
           "SFF/QUALITATIVE_REPORT.md",
           "Wenner-Gren Hunt Fellowship/QUALITATIVE_REPORT.md"]

# **1 · `ARG-4` · `INST` · `path/to/file.md`** …   (the "·"-separated proposal header)
PROPOSAL = re.compile(
    r"^\*\*(\d+[a-z]?)\s*·\s*`([A-Za-z0-9_\-]+)`\s*(?:\((?:new|#\d+)\))?\s*"
    r"(?:·\s*`([A-Za-z0-9_]+)`\s*)?·\s*`?([^`*\n]+?\.(?:md|json|yml))`?",
    re.M)
IS_NEW = re.compile(r"\(new\)")


STUB_MARKERS = ("has moved", "canonical copy:", "moved 2026-")


def is_redirect_stub(p: Path) -> bool:
    """A consolidated artifact leaves a pointer at its old path. Resolving to the pointer
    instead of the real file reports every landed proposal as missing — which is how this
    check produced seven false alarms on its first run, 2026-09-12."""
    try:
        if p.stat().st_size > 2500:
            return False
        return any(m in p.read_text(errors="replace")[:600].lower() for m in STUB_MARKERS)
    except OSError:
        return False


def resolve(target: str, roots: list[Path]) -> Path | None:
    name = Path(target.strip()).name
    candidates: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        direct = root / target.strip()
        if direct.exists():
            candidates.append(direct)
        for hit in root.rglob(name):
            if ".bak" in hit.name or "frozen-backup" in str(hit) or "retired" in hit.name:
                continue
            candidates.append(hit)
    real = [c for c in candidates if not is_redirect_stub(c)]
    if real:
        # prefer the largest — the canonical file, not a fragment
        return max(real, key=lambda c: c.stat().st_size)
    return candidates[0] if candidates else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--skill", default=str(Path(__file__).resolve().parents[1]))
    args = ap.parse_args()

    ws = Path(args.workspace).expanduser()
    skill = Path(args.skill).expanduser()
    roots = [skill, skill.parent / "voice-check", ws]

    landed, not_landed, unverifiable, unresolved = [], [], [], []

    for rel in SOURCES:
        src = ws / rel
        if not src.exists():
            continue
        text = src.read_text()
        for m in PROPOSAL.finditer(text):
            num, target_id, _scope, target_file = m.groups()
            line = text[: m.start()].count("\n") + 1
            is_new = bool(IS_NEW.search(text[m.start(): m.start() + 200]))
            dest = resolve(target_file, roots)
            rec = (Path(rel).name, line, num, target_id, target_file)
            if dest is None:
                unresolved.append(rec + ("target file not found",))
            elif target_id in dest.read_text():
                if is_new:
                    landed.append(rec + (f"`{target_id}` present in {dest.name}",))
                else:
                    unverifiable.append(rec + (f"`{target_id}` exists in {dest.name}; whether the AMENDMENT was applied needs a human",))
            else:
                not_landed.append(rec + (f"`{target_id}` ABSENT from {dest.name}",))

    def show(title, items):
        if not items:
            return
        print(f"\n{title} ({len(items)})")
        for f, line, num, tid, tf, note in items:
            print(f"  {f}:{line}  proposal {num} · {tid} → {tf}")
            print(f"      {note}")

    show("NOT LANDED — proposed, named a target, never applied", not_landed)
    show("UNRESOLVED — the named target file does not exist", unresolved)
    show("NEEDS HUMAN CONFIRMATION — amendment to an existing item", unverifiable)
    show("LANDED", landed)

    total = len(landed) + len(not_landed) + len(unverifiable) + len(unresolved)
    print(f"\nsummary: {total} proposals · {len(landed)} landed · {len(not_landed)} NOT landed · "
          f"{len(unverifiable)} need confirmation · {len(unresolved)} unresolved targets")
    if not_landed or unresolved:
        print("FAIL — a proposal that named its own target and was never applied is the "
              "failure this check exists for.")
        return 1
    print("OK — nothing proposed-and-abandoned.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
