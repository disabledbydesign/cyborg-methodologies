#!/usr/bin/env bash
# /printpress init — verify and complete the install.
#
# DEPLOYMENT MODEL: ~/.claude/skills/printpress is a SYMLINK TO THIS REPO DIRECTORY.
# One link, at the directory level. Every file in this repo is therefore already the
# file the runtime reads — there is nothing to copy and nothing to keep in sync.
#
# ⚠ 2026-09-12. A previous version of this script tried to symlink each file
# individually from the repo into the skill home. Because the skill home ALREADY
# resolved to this directory, every `ln -s X X` produced a self-referential link and
# the whole skill became unreadable in one run. Content survived only because the
# script moved the originals aside first. The guard below exists so that cannot recur:
# if the destination resolves to this directory, the install is already correct and
# there is nothing to link.
#
# Usage:
#   bash init.sh           verify; create the local-data files if missing
#   bash init.sh --check   verify only; exit 1 if the install is wrong

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P )"
SKILL_HOME="${HOME}/.claude/skills/printpress"

CHECK=0
for arg in "$@"; do
  case "$arg" in
    --check) CHECK=1 ;;
    -h|--help) sed -n '1,20p' "$0"; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

echo "/printpress init"
echo "  repo:       ${SCRIPT_DIR}"
echo "  skill home: ${SKILL_HOME}"
echo

PROBLEMS=0

# ── 1. The one thing that matters: does the skill home resolve to this repo? ──
if [ ! -e "${SKILL_HOME}" ]; then
  echo "[MISSING] ${SKILL_HOME} does not exist."
  echo "          Create the deployment link:"
  echo "            mkdir -p \"${HOME}/.claude/skills\""
  echo "            ln -s \"${SCRIPT_DIR}\" \"${SKILL_HOME}\""
  PROBLEMS=$((PROBLEMS + 1))
else
  RESOLVED="$( cd "${SKILL_HOME}" && pwd -P )"
  if [ "${RESOLVED}" = "${SCRIPT_DIR}" ]; then
    echo "[ok] skill home resolves to this repo — the deployment link is correct"
    echo "     every repo edit is live at the runtime path, with no copy step"
  else
    echo "[WRONG] ${SKILL_HOME} resolves to:"
    echo "          ${RESOLVED}"
    echo "        but this repo is:"
    echo "          ${SCRIPT_DIR}"
    echo "        The runtime is reading a different tree than the one you are editing."
    echo "        Fix by replacing the skill home with a link to this repo:"
    echo "            mv \"${SKILL_HOME}\" \"${SKILL_HOME}.old-\$(date +%Y%m%d-%H%M%S)\""
    echo "            ln -s \"${SCRIPT_DIR}\" \"${SKILL_HOME}\""
    PROBLEMS=$((PROBLEMS + 1))
  fi
fi

# ── 2. Local data that must NOT be symlinked and must NOT be committed ───────
# These live in the repo directory (which is the skill home) but are gitignored.
if [ "$CHECK" = 0 ]; then
  if [ ! -d "${SCRIPT_DIR}/profiles" ]; then
    mkdir -p "${SCRIPT_DIR}/profiles"
    cat > "${SCRIPT_DIR}/profiles/.gitignore" <<'EOF'
# Author profiles contain personal data — never commit.
*
!.gitignore
EOF
    echo "[ok] profiles/ (with .gitignore)"
  else
    echo "[skip] profiles/ already exists"
  fi

  if [ ! -f "${SCRIPT_DIR}/other_log.md" ]; then
    cat > "${SCRIPT_DIR}/other_log.md" <<'EOF'
# /printpress — `other` genre accumulation log

<!--
SPEC.md § Learning loops, Tier 2. Each /printpress invocation resolving to the `other`
genre logs an entry. The skill reads this at Stage 0 on every `other` invocation; on the
3rd-or-later use it surfaces the genre-promotion proposal before proceeding.

Per entry: date · document type · who reads this · source material · swarm composition ·
what worked / didn't · promoted to genre (or "—").
-->

## Entries

*(No `other` invocations logged yet.)*
EOF
    echo "[ok] other_log.md"
  else
    echo "[skip] other_log.md already exists"
  fi
fi

# ── 3. Sanity: the files the skill actually needs are present ────────────────
for required in SKILL.md SPEC.md genre_configs templates tools; do
  if [ ! -e "${SCRIPT_DIR}/${required}" ]; then
    echo "[MISSING] ${required} is not in the repo"
    PROBLEMS=$((PROBLEMS + 1))
  elif [ -L "${SCRIPT_DIR}/${required}" ]; then
    # A symlink here is the 2026-09-12 self-link bug, or a stray.
    if [ ! -e "${SCRIPT_DIR}/${required}" ]; then
      echo "[BROKEN] ${required} is a dangling symlink — restore it from a .frozen-backup-* sibling"
      PROBLEMS=$((PROBLEMS + 1))
    fi
  fi
done

echo
if [ "$PROBLEMS" -gt 0 ]; then
  echo "${PROBLEMS} problem(s). See above."
  exit 1
fi
echo "install correct."
