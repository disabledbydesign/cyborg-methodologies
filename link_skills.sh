#!/usr/bin/env bash
# link_skills.sh — make ~/.claude/skills/<name> a symlink to this repo's <name>/
#
# THE MODEL: skills live here, in version control. ~/.claude/skills holds symlinks.
# One copy, one history, and an edit in either place is the same edit.
#
# ⚠ WHY THIS SCRIPT IS PARANOID. On 2026-09-12 a script assumed ~/.claude/skills/printpress
# was a real directory, when it was already a symlink to this repo. Every `ln -s X X` it
# created pointed at itself and the whole skill became unreadable in one run. Content
# survived only because the originals had been moved aside first. Separately, the
# voice-check profile turned out to exist ONLY under ~/.claude — the installed copy held
# 237 KB that was in no repository. Either mistake, run blind, destroys work.
#
# So: this script REPORTS by default and changes nothing. With --migrate it will replace a
# real directory with a symlink ONLY when the repo already contains everything that
# directory has. If the installed copy has any file the repo lacks, or any file whose
# content differs, it STOPS for that skill and tells you what to reconcile first.
#
#   bash link_skills.sh              report what each skill is; change nothing
#   bash link_skills.sh --migrate    link the ones that are provably safe
#   bash link_skills.sh --migrate --skill critic-swarm    just one
#   bash link_skills.sh --show-ignored   also list what the comparison skipped

set -euo pipefail

REPO="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P )"
SKILLS="${HOME}/.claude/skills"
MIGRATE=0
ONLY=""
SHOW_IGNORED=0

while [ $# -gt 0 ]; do
  case "$1" in
    --migrate) MIGRATE=1 ;;
    --skill) ONLY="${2:-}"; shift ;;
    --show-ignored) SHOW_IGNORED=1 ;;
    -h|--help) sed -n '1,26p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

# Shared definition of what counts as work vs. regenerable noise.
source "${REPO}/skills_common.sh"

echo "repo:   ${REPO}"
echo "skills: ${SKILLS}"
[ "$MIGRATE" = 1 ] && echo "mode:   --migrate (will link only what is provably safe)" \
                   || echo "mode:   report only — nothing will change"
echo "ignore: $(ignore_summary)"
echo

[ -d "$SKILLS" ] || { echo "no ${SKILLS} — nothing to do"; exit 1; }

BLOCKED=0; LINKED=0; ALREADY=0; SKIPPED=0

for repo_skill in "$REPO"/*/; do
  name="$(basename "$repo_skill")"
  case "$name" in .*|contexts|samples|sessions|graphify-out) continue ;; esac
  [ -f "${repo_skill}SKILL.md" ] || continue          # only real skills
  [ -n "$ONLY" ] && [ "$ONLY" != "$name" ] && continue

  installed="${SKILLS}/${name}"
  target="${repo_skill%/}"

  if [ ! -e "$installed" ] && [ ! -L "$installed" ]; then
    echo "  ${name}: NOT INSTALLED"
    if [ "$MIGRATE" = 1 ]; then
      ln -s "$target" "$installed"; echo "      -> linked"; LINKED=$((LINKED+1))
    else
      echo "      would link -> ${target}"
    fi
    continue
  fi

  if [ -L "$installed" ]; then
    dest="$( cd "$installed" 2>/dev/null && pwd -P || readlink "$installed" )"
    if [ "$dest" = "$target" ]; then
      echo "  ${name}: already linked to this repo ✓"; ALREADY=$((ALREADY+1))
    else
      echo "  ${name}: SYMLINK TO SOMEWHERE ELSE"
      echo "      -> ${dest}"
      echo "      not touching it; resolve by hand"
      BLOCKED=$((BLOCKED+1))
    fi
    continue
  fi

  # A real directory. Compare before considering replacement.
  echo "  ${name}: REAL DIRECTORY — the repo copy is not in service"

  counted="$(list_files "$installed" | wc -l | tr -d ' ')"
  total="$(count_all "$installed")"
  echo "      comparing ${counted} of ${total} installed files ($((total - counted)) ignored as regenerable)"

  only_installed="$(comm -13 <(list_files "$target") <(list_files "$installed") || true)"
  differing=""
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    if [ -f "${target}/${f}" ] && ! cmp -s "${installed}/${f}" "${target}/${f}"; then
      differing="${differing}${f}"$'\n'
    fi
  done < <(list_files "$installed")

  if [ "$SHOW_IGNORED" = 1 ]; then
    echo "      ignored here:"
    ( cd "$installed" && find . -type f 2>/dev/null ) | LC_ALL=C sort \
      | comm -23 - <(list_files "$installed") \
      | sed 's|^\./||' | awk -F/ '{print $1"/"$2}' | sort -u | sed 's/^/           /' | head -20
  fi

  if [ -n "$only_installed" ] || [ -n "$differing" ]; then
    echo "      ⛔ BLOCKED — the installed copy holds work the repo does not:"
    [ -n "$only_installed" ] && { echo "         files only in ~/.claude:"; echo "$only_installed" | sed 's/^/           /'; }
    [ -n "$differing" ]      && { echo "         files whose content differs:"; echo "$differing" | sed 's/^/           /'; }
    echo "      Run  bash rescue_skill.sh ${name}  to copy them in, then commit and re-run."
    BLOCKED=$((BLOCKED+1)); continue
  fi

  echo "      repo contains everything the installed copy has — safe to link"
  if [ "$MIGRATE" = 1 ]; then
    backup="${installed}.pre-link-$(date +%Y%m%d-%H%M%S)"
    mv "$installed" "$backup"
    ln -s "$target" "$installed"
    echo "      -> linked (previous directory kept as $(basename "$backup"))"
    LINKED=$((LINKED+1))
  else
    echo "      would link -> ${target}"; SKIPPED=$((SKIPPED+1))
  fi
done

echo
echo "already linked: ${ALREADY}   linked now: ${LINKED}   blocked: ${BLOCKED}   pending: ${SKIPPED}"
[ "$BLOCKED" -gt 0 ] && { echo "Resolve the blocked ones by hand — they hold work that exists nowhere else."; exit 1; }
[ "$MIGRATE" = 0 ] && [ "$SKIPPED" -gt 0 ] && echo "Re-run with --migrate to link the safe ones."
exit 0
