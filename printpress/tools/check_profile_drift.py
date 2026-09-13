#!/usr/bin/env python3
"""check_profile_drift.py — has an applied check drifted from the profile that defines it?

A voice-check profile defines each prose check once. A style review then APPLIES those
checks to a real draft, and in doing so restates each one — "What it asks for." That
restatement is where drift enters: it is a summary, written under the pressure of one
specific document, and the next reviewer who reads the summary instead of the profile
inherits the compression.

Measured on 2026-09-13, comparing `Spelman/STYLE_REVIEW_v11.md` against profile v3.13:
**median text similarity 0.11, and the restatements totalled 19% of the profile's text.**
Every operational test, anti-pattern and author example was gone — the four features of
`topic_sentence_craft` survived as a list; the test that makes them usable ("if the sentence
could be replaced with 'The following paragraph discusses X,' it is meta") did not. No
content was unique to the restatement. A profile rebuilt from such a review would read
complete and be operationally hollow.

So this tool does not rebuild. It compares, and reports where a review's wording has
diverged far enough from the profile that a reader of one would not be applying the other.

    python3 check_profile_drift.py --profile PATH --review PATH [--threshold 0.4]

Exit 1 if any check falls below the threshold, or if a review names an id the profile
does not define (a check invented during application — the other direction of the same
failure).

*Was `rebuild_profile.py`, written 2026-09-12 to reconstruct a profile believed lost. The
profile was not lost; the belief came from a sandbox that cannot read `~/.claude`. The
extraction machinery turned out to be useful for the opposite job.*
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

CHECK_HEAD = re.compile(r"^## (\d+)\.\s+`([a-z0-9_]+)`\s*$", re.M)
ASKS = re.compile(r"\*\*What it asks for\.\*\*\s*(.+?)(?=\n\s*\n\*\*|\Z)", re.S)

# Text that only a definition carries: a test you can run, an anti-pattern, an example in
# the author's own words. Losing ANY of these is drift regardless of how similar the
# wording looks — a check you cannot apply to a sentence has stopped doing its job.
OPERATIONAL = ("TEST:", "Anti-pattern", "NOT '", 'NOT "', "e.g.", "June:", "TEST —")


def flat(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


def review_checks(path: Path) -> dict[str, str]:
    text = path.read_text()
    heads = list(CHECK_HEAD.finditer(text))
    out: dict[str, str] = {}
    for i, m in enumerate(heads):
        body = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        a = ASKS.search(body)
        if a:
            out[m.group(2)] = flat(a.group(1))
    return out


def profile_checks(path: Path, role: str | None) -> dict[str, str]:
    data = json.loads(path.read_text())
    return {c["id"]: flat(c.get("instruction"))
            for c in data.get("qualitative", [])
            if role is None or c.get("role") == role}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", required=True, help="the profile that DEFINES the checks")
    ap.add_argument("--review", required=True, help="a style review that APPLIES them")
    ap.add_argument("--role", default="pre_draft", help="profile role to compare (default pre_draft)")
    ap.add_argument("--threshold", type=float, default=0.40)
    args = ap.parse_args()

    prof = profile_checks(Path(args.profile).expanduser(), args.role or None)
    rev = review_checks(Path(args.review).expanduser())
    if not rev:
        print("no checks found in the review — is it a style review with '## N. `id`' headings?",
              file=sys.stderr)
        return 2

    undefined = sorted(set(rev) - set(prof))
    shared = [cid for cid in rev if cid in prof]

    rows = []
    for cid in shared:
        p, r = prof[cid], rev[cid]
        sim = difflib.SequenceMatcher(None, p.lower(), r.lower()).ratio()
        lost = [t for t in OPERATIONAL if t in p and t not in r]
        rows.append((sim, cid, len(p), len(r), lost))
    rows.sort()

    # Similarity alone is not enough. A restatement that quotes the opening sentence
    # verbatim and drops the TEST scores high and is still unusable — the operational
    # content is what lets a check change a sentence. Found by the test suite, 2026-09-13.
    drifted = [x for x in rows if x[0] < args.threshold or x[4]]

    print(f"profile: {Path(args.profile).name}   review: {Path(args.review).name}")
    print(f"  {len(shared)} checks compared · role={args.role}\n")
    print(f"  {'sim':>5}  {'check':34s} {'def':>6} {'applied':>7}  operational content dropped")
    for sim, cid, pl, rl, lost in rows:
        mark = "  DRIFT" if (sim < args.threshold or lost) else ""
        print(f"  {sim:5.2f}  {cid:34s} {pl:6d} {rl:7d}  "
              f"{', '.join(lost) if lost else '—'}{mark}")

    tp = sum(x[2] for x in rows) or 1
    tr = sum(x[3] for x in rows)
    print(f"\n  applied text is {tr/tp:.0%} of the definition text "
          f"({tr:,} / {tp:,} chars)")
    if undefined:
        print(f"\n  ⚠ named in the review but NOT DEFINED in the profile ({len(undefined)}): "
              f"{', '.join(undefined)}")
        print("    a check invented during application is the same failure running the other way.")
    low = sum(1 for x in rows if x[0] < args.threshold)
    stripped = sum(1 for x in rows if x[4])
    print(f"\n  {len(drifted)} of {len(shared)} drifted "
          f"({low} below the {args.threshold:.2f} similarity threshold, "
          f"{stripped} with operational content dropped)")

    if drifted or undefined:
        print("\nFAIL — a reader of the review is not applying the profile. Either the review "
              "should quote the definition, or the profile should absorb what the review learned. "
              "Do not resolve it by replacing the definition with the restatement.")
        return 1
    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
