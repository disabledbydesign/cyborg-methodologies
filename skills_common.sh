#!/usr/bin/env bash
# skills_common.sh — one definition of "what counts as work" for the skill scripts.
#
# Sourced by link_skills.sh and rescue_skill.sh. It exists so the two cannot
# disagree about which files matter — the same class of drift these scripts are
# here to prevent.
#
# Noise is anything a tool regenerates from something else: virtualenvs, caches,
# compiled bytecode, Finder droppings, timestamped backups. A .venv/ holding
# 3,000 files of numpy and spacy is not work that exists nowhere else — it is
# `pip install` output, and blocking on it hides the one file that actually
# differs. Ignoring is never deleting: link_skills.sh --migrate keeps the entire
# previous directory as <name>.pre-link-<timestamp>.

PRUNE_DIRS=(.git .venv venv env node_modules __pycache__ .pytest_cache
            .mypy_cache .ruff_cache .ipynb_checkpoints .tox)
IGNORE_FILES=('*.pyc' '*.pyo' '.DS_Store' '*.egg-info' '*.bak' '*.bak.*'
              '*.orig' '*.rej' '*~')

# list_files <dir> — files that count, as ./relative/paths, sorted
list_files() {
  local d="$1" args=() first=1 p
  for p in "${PRUNE_DIRS[@]}"; do
    if [ $first = 1 ]; then args+=( '(' -name "$p" ); first=0
    else args+=( -o -name "$p" ); fi
  done
  args+=( ')' -prune -o -type f )
  for p in "${IGNORE_FILES[@]}"; do args+=( ! -name "$p" ); done
  args+=( -print )
  ( cd "$d" && find . "${args[@]}" 2>/dev/null | LC_ALL=C sort )
}

# count_all <dir> — every file, for reporting how much was skipped
count_all() { ( cd "$1" && find . -type f 2>/dev/null | wc -l | tr -d ' ' ); }

ignore_summary() { echo "${PRUNE_DIRS[*]} + ${IGNORE_FILES[*]}"; }
