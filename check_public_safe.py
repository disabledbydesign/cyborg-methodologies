#!/usr/bin/env python3
"""Refuse to push personal material from a public repository.

CLAUDE.md has carried this rule since the repo was created:

    Before any push, run a grep for personal identifiers (usernames, real names,
    local paths) from repo root. Must return nothing. Keep the specific grep
    pattern in your local HANDOFF.md, not in this public file.

It was broken on 2026-09-12 — a push added nine files containing /Users/june/
paths naming four private repositories. The rule failed for a structural reason,
not a careless one: HANDOFF.md is gitignored, so the pattern it told you to use
lives nowhere any agent or fresh checkout can read it. An instruction whose
content is unreachable is not an instruction.

So the pattern lives here, executable, and runs from a pre-push hook.

THE DISTINCTION IT DRAWS. Not everything personal is a leak. June's name is on
this work and belongs on it; her writing profile is a detailed model of how she
writes, built from unpublished drafts, and does not. So:

  BLOCK  files that are a model of the person — voice profiles, the profile
         change log, audits of it, extracts from it — and anything shaped like a
         live credential. These must never enter a public history, and unlike a
         working-tree mistake, a push cannot be taken back.

  WARN   absolute home paths. They leak the names of private repositories and
         break if the tree moves, but they are already throughout the history
         and blocking on them would just train you to pass --no-verify.

    python3 check_public_safe.py            # check tracked + staged files
    python3 check_public_safe.py --install   # install the pre-push hook
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Module-level default; --repo overrides it so the check can be tested against a
# fixture instead of whatever tree the script happens to sit in.
REPO = Path(__file__).resolve().parent

# A model of the person, not of the method.
BLOCKED_PATHS = [
    re.compile(r"(^|/)profiles/(?!base\.json$)[^/]+\.json$"),
    re.compile(r"(^|/)PROFILE_CHANGE_LOG\.md$"),
    re.compile(r"(^|/)AUDIT_REPORT_[\d-]+\.md$"),
    re.compile(r"(^|/)AGENT_FEEDBACK_[\d-]+\.md$"),
    re.compile(r"(^|/)TEST_B_PREDRAFT_EXTRACT\.json$"),
    re.compile(r"(^|/)VOICE_DOCUMENT\.md$"),
    re.compile(r"(^|/)JUNE_BLOCH_AGENT_BRIEFING\.md$"),
]

# Shaped like a live secret. Test fixtures ("app-password") are excluded below.
SECRETS = [
    (re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"), "Anthropic API key"),
    (re.compile(r"\bAKIA[A-Z0-9]{16}\b"), "AWS access key id"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"), "GitHub token"),
    (re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"), "private key"),
]
SECRET_FALSE_POSITIVE = re.compile(
    r"(app-password|deliberately-wrong|example|placeholder|your[_-]|<[a-z_]+>|"
    r"getenv|environ|test[_-])", re.I)

HOME_PATH = re.compile(r"/Users/[A-Za-z0-9_.-]+/")

TEXT_SUFFIXES = {".md", ".py", ".sh", ".json", ".yml", ".yaml", ".txt", ".html",
                 ".js", ".ini", ".cfg", ".toml"}


def git(*args: str) -> list[str]:
    out = subprocess.run(["git", "-C", str(REPO), *args],
                         capture_output=True, text=True)
    return [l for l in out.stdout.splitlines() if l.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--install", action="store_true", help="install the pre-push hook")
    ap.add_argument("--repo", type=Path, help="check this repository instead of this script's own")
    args = ap.parse_args()

    global REPO
    if args.repo:
        REPO = args.repo.resolve()

    if args.install:
        hook = REPO / ".git" / "hooks" / "pre-push"
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text("#!/bin/sh\n"
                        "# Installed by check_public_safe.py --install\n"
                        'exec python3 "$(git rev-parse --show-toplevel)/check_public_safe.py"\n')
        hook.chmod(0o755)
        print(f"pre-push hook installed at {hook}")
        print("It runs on every push. `git push --no-verify` skips it.")
        return 0

    files = sorted(set(git("ls-files")))
    blocked, secrets, home_paths = [], [], []

    for rel in files:
        for pat in BLOCKED_PATHS:
            if pat.search(rel):
                blocked.append(rel)
                break
        p = REPO / rel
        if p.suffix.lower() not in TEXT_SUFFIXES or not p.is_file():
            continue
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            for pat, label in SECRETS:
                if pat.search(line) and not SECRET_FALSE_POSITIVE.search(line):
                    secrets.append((rel, label))
        if HOME_PATH.search(text):
            home_paths.append(rel)

    if home_paths:
        print(f"WARN: {len(home_paths)} tracked file(s) contain absolute /Users/ paths.")
        print("      They name private repositories and break if the tree moves.")
        for rel in home_paths[:10]:
            print(f"        {rel}")
        if len(home_paths) > 10:
            print(f"        … and {len(home_paths) - 10} more")
        print()

    if not blocked and not secrets:
        print("OK — no personal profile material and nothing shaped like a credential.")
        return 0

    print("REFUSING THE PUSH. This repository is public, and a push cannot be undone.")
    for rel in sorted(set(blocked)):
        print(f"  personal profile material: {rel}")
    for rel, label in sorted(set(secrets)):
        print(f"  possible {label}: {rel}")
    print("\nThese belong in the private Job Search repo, symlinked back if a tool")
    print("names the path. See voice_profiles/README.md there.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
