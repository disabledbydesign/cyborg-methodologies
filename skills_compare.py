#!/usr/bin/env python3
"""Compare an installed skill directory against its copy in this repository.

THE SINGLE DEFINITION of what counts as work, and the only comparison the skill
scripts are allowed to use. link_skills.sh and rescue_skill.sh both call it, so
the two cannot disagree about what is missing — the class of drift they exist to
prevent.

WHY THIS IS PYTHON AND NOT SHELL. It was `find | sort | comm`, and it silently
reported wrong answers on macOS. `sort` ran under LC_ALL=C; `comm` compares using
the *current* locale's collation. Under en_US.UTF-8 those two orderings disagree
about where uppercase stops and lowercase starts, so comm hit what it considered
disordered input at the first lowercase filename and mis-reported every shared
file after that point as missing. The warning went to stderr, where `|| true`
swallowed it. rescue_skill.sh then "restored" eight files the repository already
had, overwriting one of them.

That failure is invisible, locale-dependent, and lands on the exact operation
these scripts exist to make safe. So the comparison lives here, where the walk,
the ordering and the symlink handling are explicit and identical everywhere.

Usage:
    python3 skills_compare.py REPO_DIR INSTALLED_DIR       # human-readable
    python3 skills_compare.py REPO_DIR INSTALLED_DIR --json
    python3 skills_compare.py --ignore-summary
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from fnmatch import fnmatch
from pathlib import Path

# Noise is anything a tool regenerates from something else. A .venv/ holding
# 3,000 files of numpy is not work that exists nowhere else — it is `pip install`
# output, and blocking a migration on it hides the one file that really differs.
# Ignoring is never deleting: link_skills.sh --migrate keeps the entire previous
# directory as <name>.pre-link-<timestamp>.
PRUNE_DIRS = {".git", ".venv", "venv", "env", "node_modules", "__pycache__",
              ".pytest_cache", ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints",
              ".tox"}
IGNORE_GLOBS = ("*.pyc", "*.pyo", ".DS_Store", "*.egg-info", "*.bak", "*.bak.*",
                "*.installed-copy", "*.orig", "*.rej", "*~")


def ignored(name: str) -> bool:
    return any(fnmatch(name, g) for g in IGNORE_GLOBS)


def walk(root: Path) -> tuple[dict[str, Path], int]:
    """Map relative path -> full path, for files that count. Also the total seen.

    A SYMLINK IS A PRESENT FILE. The repository's voice-check/profiles/june_bloch.json
    is a symlink to the private copy in the Job Search workspace. Counted as absent,
    it reads as missing from the repo, and the "restore" writes the older installed
    copy straight through the link onto the newer private file.
    """
    found: dict[str, Path] = {}
    total = 0
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        # `total` counts everything, INCLUDING what is about to be pruned. The
        # whole value of the line "comparing 22 of 522 (500 ignored)" is telling
        # the reader that 500 files of pip output were skipped on purpose. Count
        # first, prune second.
        total += len(filenames)
        pruned = [d for d in dirnames if d in PRUNE_DIRS]
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS]
        for d in pruned:
            for _, _, fns in os.walk(Path(dirpath) / d, followlinks=False):
                total += len(fns)
        for fn in filenames:
            if ignored(fn):
                continue
            full = Path(dirpath) / fn
            found[str(full.relative_to(root))] = full
    return found, total


def digest(p: Path) -> str | None:
    """Content hash. None when the path cannot be read — a broken symlink, say."""
    try:
        with open(p, "rb") as fh:
            h = hashlib.sha256()
            for chunk in iter(lambda: fh.read(1 << 16), b""):
                h.update(chunk)
            return h.hexdigest()
    except OSError:
        return None


def same_file(a: Path, b: Path) -> bool:
    """Already one file on disk — a hard link, or two symlinks to one target.

    macOS `cp` refuses this with a non-zero exit ("are identical"), which under
    `set -e` killed rescue_skill.sh halfway through its copies.
    """
    try:
        return os.path.realpath(a) == os.path.realpath(b) or os.path.samefile(a, b)
    except OSError:
        return False


def compare(repo: Path, installed: Path) -> dict:
    repo_files, _ = walk(repo)
    inst_files, inst_total = walk(installed)

    missing, differing, identical = [], [], []
    for rel, inst_path in sorted(inst_files.items()):
        repo_path = repo_files.get(rel)
        if repo_path is None:
            missing.append(rel)
        elif same_file(repo_path, inst_path):
            identical.append(rel)
        elif digest(repo_path) == digest(inst_path) and digest(inst_path) is not None:
            identical.append(rel)
        else:
            differing.append(rel)

    return {
        "missing": missing,          # only in the installed copy — safe to bring in
        "differing": differing,      # two real versions — a person must choose
        "identical": identical,
        "counted": len(inst_files),
        "total": inst_total,
        "ignored": inst_total - len(inst_files),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", nargs="?", type=Path)
    ap.add_argument("installed", nargs="?", type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--ignore-summary", action="store_true")
    args = ap.parse_args()

    if args.ignore_summary:
        print(" ".join(sorted(PRUNE_DIRS)) + " + " + " ".join(IGNORE_GLOBS))
        return 0
    if not args.repo or not args.installed:
        ap.error("REPO_DIR and INSTALLED_DIR are required")

    result = compare(args.repo, args.installed)
    if args.json:
        print(json.dumps(result))
    else:
        print(f"counted {result['counted']} of {result['total']} "
              f"({result['ignored']} ignored as regenerable)")
        for rel in result["missing"]:
            print(f"  only in installed: {rel}")
        for rel in result["differing"]:
            print(f"  differs:           {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
