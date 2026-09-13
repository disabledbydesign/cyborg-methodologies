#!/usr/bin/env bash
# rescue_skill.sh — copy work that exists only in ~/.claude/skills/<name> into this repo.
#
# The companion to link_skills.sh. When that script BLOCKS a skill, this is what
# unblocks it: it brings the installed-only files into version control so the
# switch to a symlink loses nothing.
#
# It is deliberately timid about disagreement. A file the repo LACKS is copied
# straight in — there is no competing version, so there is no decision to make.
# A file whose content DIFFERS is never overwritten: it lands beside the repo
# file as <file>.installed-copy for you to diff and resolve by hand. Choosing
# between two real versions is a judgement, not a file operation.
#
#   bash rescue_skill.sh voice-check           report; change nothing
#   bash rescue_skill.sh voice-check --apply   copy the missing files in
#   bash rescue_skill.sh --all --apply         every blocked skill

set -euo pipefail

REPO="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P )"
source "${REPO}/skills_common.sh"
SKILLS="${SKILLS_DIR:-${HOME}/.claude/skills}"   # SKILLS_DIR override exists so these scripts can be tested against a fixture
APPLY=0
NAMES=()

while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1 ;;
    --all)   NAMES=(__ALL__) ;;
    -h|--help) sed -n '1,20p' "$0"; exit 0 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) NAMES+=("$1") ;;
  esac
  shift
done

[ ${#NAMES[@]} -gt 0 ] || { echo "usage: bash rescue_skill.sh <skill-name>... [--apply]" >&2; exit 2; }

if [ "${NAMES[0]}" = "__ALL__" ]; then
  NAMES=()
  for d in "$REPO"/*/; do
    n="$(basename "$d")"
    case "$n" in .*|contexts|samples|sessions|graphify-out) continue ;; esac
    [ -f "${d}SKILL.md" ] || continue
    [ -d "${SKILLS}/${n}" ] && [ ! -L "${SKILLS}/${n}" ] && NAMES+=("$n")
  done
fi

echo "repo:   ${REPO}"
echo "skills: ${SKILLS}"
[ "$APPLY" = 1 ] && echo "mode:   --apply (will copy files in)" || echo "mode:   report only — nothing will change"
echo "ignore: $(ignore_summary)"
echo

COPIED=0; CONFLICTS=0

for name in "${NAMES[@]}"; do
  installed="${SKILLS}/${name}"
  target="${REPO}/${name}"
  echo "  ${name}"
  if [ ! -d "$installed" ]; then echo "      no installed copy — nothing to rescue"; continue; fi
  if [ -L "$installed" ]; then echo "      already a symlink — nothing to rescue"; continue; fi
  [ -d "$target" ] || { echo "      no repo directory ${target} — refusing to guess"; continue; }

  missing="$(comm -13 <(list_files "$target") <(list_files "$installed") || true)"
  differing=""
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    if [ -f "${target}/${f}" ] && ! cmp -s "${installed}/${f}" "${target}/${f}"; then
      differing="${differing}${f}"$'\n'
    fi
  done < <(list_files "$installed")

  n_missing=0; [ -n "$missing" ] && n_missing=$(echo "$missing" | grep -c . || true)
  n_diff=0;    [ -n "$differing" ] && n_diff=$(echo "$differing" | grep -c . || true)
  echo "      ${n_missing} file(s) only in ~/.claude, ${n_diff} file(s) differing"

  if [ -n "$missing" ]; then
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      if [ "$APPLY" = 1 ]; then
        mkdir -p "$(dirname "${target}/${f}")"
        cp -p "${installed}/${f}" "${target}/${f}"
        echo "      + ${f#./}"
        COPIED=$((COPIED+1))
      else
        echo "      would copy: ${f#./}"
      fi
    done <<< "$missing"
  fi

  if [ -n "$differing" ]; then
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      if [ "$APPLY" = 1 ]; then
        cp -p "${installed}/${f}" "${target}/${f}.installed-copy"
        echo "      ? ${f#./}  -> staged as ${f#./}.installed-copy (resolve by hand)"
      else
        echo "      would stage for review: ${f#./}"
      fi
      CONFLICTS=$((CONFLICTS+1))
    done <<< "$differing"
  fi
done

echo
if [ "$APPLY" = 1 ]; then
  echo "copied: ${COPIED}   staged for review: ${CONFLICTS}"
  [ "$CONFLICTS" -gt 0 ] && echo "Diff each *.installed-copy, keep one, delete the other, then commit."
  echo "Then: git add -A && git commit  — and re-run link_skills.sh"
else
  echo "Nothing changed. Re-run with --apply."
fi
exit 0
