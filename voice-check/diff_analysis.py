"""
Diff analysis for voice-check --learn pipeline.

Computes sentence-level and paragraph-level differences between two draft versions.
Detects change types (preserved/edited/rewritten/added/deleted) and structural moves.

Standalone usage:
    python3 diff_analysis.py FIRST_DRAFT FINAL_DRAFT
"""

import re
import sys
from difflib import SequenceMatcher

try:
    from nltk.tokenize import sent_tokenize
    _HAS_NLTK = True
except ImportError:
    _HAS_NLTK = False


# ---------------------------------------------------------------------------
# Text splitting
# ---------------------------------------------------------------------------

def split_sentences(text: str) -> list:
    """Split text into sentences. Uses nltk if available, else regex fallback."""
    text = text.strip()
    if not text:
        return []
    if _HAS_NLTK:
        try:
            return [s.strip() for s in sent_tokenize(text) if s.strip()]
        except Exception:
            pass
    # Regex fallback: split on .!? followed by whitespace and capital letter
    raw = re.split(r'(?<=[.!?])\s+(?=[A-Z\"])', text)
    return [s.strip() for s in raw if s.strip()]


def split_paragraphs(text: str) -> list:
    """Split text into paragraphs by double newlines. Skip very short entries."""
    paras = re.split(r'\n{2,}', text.strip())
    result = []
    for p in paras:
        p = p.strip()
        if len(p.split()) >= 5:  # skip headers and near-empty lines
            result.append(p)
    return result


# ---------------------------------------------------------------------------
# Similarity
# ---------------------------------------------------------------------------

def _normalize(s: str) -> str:
    """Lowercase and collapse whitespace for comparison."""
    return re.sub(r'\s+', ' ', s.lower().strip())


def sentence_similarity(s1: str, s2: str) -> float:
    """Return 0.0–1.0 similarity between two sentences using SequenceMatcher."""
    n1, n2 = _normalize(s1), _normalize(s2)
    if not n1 and not n2:
        return 1.0
    if not n1 or not n2:
        return 0.0
    return SequenceMatcher(None, n1, n2).ratio()


def paragraph_similarity(p1: str, p2: str) -> float:
    """Similarity between two paragraphs using SequenceMatcher on full text."""
    return SequenceMatcher(None, _normalize(p1), _normalize(p2)).ratio()


# ---------------------------------------------------------------------------
# Sentence alignment and classification
# ---------------------------------------------------------------------------

def align_sentences(first_sents: list, final_sents: list, threshold: float = 0.4) -> list:
    """
    Fuzzy best-match alignment: for each first-draft sentence, find the best-matching
    final-draft sentence above the threshold. Sentences without a match are deleted/added.

    Returns list of (tag, first_idx_or_None, final_idx_or_None, similarity).
    Tags: 'equal' (sim>=0.95), 'replace' (matched but changed), 'delete', 'insert'
    """
    if not first_sents and not final_sents:
        return []

    # Build similarity matrix
    matched_final = {}  # final_idx -> (first_idx, similarity)
    matched_first = {}  # first_idx -> (final_idx, similarity)

    # Greedy best-match — sort all candidate pairs by similarity, claim greedily
    candidates = []
    for i, fs in enumerate(first_sents):
        for j, ls in enumerate(final_sents):
            sim = sentence_similarity(fs, ls)
            if sim >= threshold:
                candidates.append((sim, i, j))
    candidates.sort(reverse=True)  # highest similarity first

    for sim, i, j in candidates:
        if i in matched_first or j in matched_final:
            continue
        matched_first[i] = (j, sim)
        matched_final[j] = (i, sim)

    # Build aligned list. Matches and deletes preserve first-draft order;
    # inserts (unmatched final sentences) are appended at the end.
    aligned = []
    for i in range(len(first_sents)):
        if i in matched_first:
            j, sim = matched_first[i]
            tag = 'equal' if sim >= 0.95 else 'replace'
            aligned.append((tag, i, j, sim))
        else:
            aligned.append(('delete', i, None, 0.0))

    for j in range(len(final_sents)):
        if j not in matched_final:
            aligned.append(('insert', None, j, 0.0))

    return aligned


def classify_sentence_pair(s1: str, s2: str, sim: float) -> str:
    """Classify a sentence change by similarity score."""
    if sim >= 0.9:
        return 'preserved'
    elif sim >= 0.7:
        return 'light_edit'
    elif sim >= 0.4:
        return 'substantial_rewrite'
    else:
        return 'substantial_rewrite'  # very different — still a rewrite, not delete/add


# ---------------------------------------------------------------------------
# Paragraph move detection
# ---------------------------------------------------------------------------

def detect_paragraph_moves(first_paras: list, final_paras: list, threshold: float = 0.6) -> list:
    """
    Detect paragraphs that appear in a different position in the final vs. first draft.
    Returns list of {first_position, final_position, similarity, preview}.
    Only reports paragraphs that moved by at least 2 positions.
    """
    moves = []
    # For each final paragraph, find best match in first
    used_first = set()
    for j, fp in enumerate(final_paras):
        best_sim, best_i = 0.0, -1
        for i, pp in enumerate(first_paras):
            if i in used_first:
                continue
            sim = paragraph_similarity(pp, fp)
            if sim > best_sim:
                best_sim, best_i = sim, i
        if best_sim >= threshold and best_i >= 0:
            used_first.add(best_i)
            if abs(best_i - j) >= 2:  # only flag meaningful moves
                preview = fp[:80].replace('\n', ' ') + ('...' if len(fp) > 80 else '')
                moves.append({
                    'first_position': best_i + 1,
                    'final_position': j + 1,
                    'similarity': round(best_sim, 3),
                    'preview': preview,
                })
    return moves


# ---------------------------------------------------------------------------
# Master function
# ---------------------------------------------------------------------------

def compute_diff(first_text: str, final_text: str) -> dict:
    """
    Compute a structured diff between two draft versions.

    Returns:
        sentence_changes: dict with counts by category
        change_rate: float, % of first-draft sentences substantially changed or deleted
        paragraph_moves: list of moved paragraph dicts
        notable_rewrites: top 5 most-changed sentence pairs
        structural_vs_local: 'structural' if para moves dominate, else 'local'
        total_first_sentences: int
        total_final_sentences: int
    """
    first_sents = split_sentences(first_text)
    final_sents = split_sentences(final_text)
    first_paras = split_paragraphs(first_text)
    final_paras = split_paragraphs(final_text)

    aligned = align_sentences(first_sents, final_sents)

    changes = {'preserved': 0, 'light_edit': 0, 'substantial_rewrite': 0, 'deleted': 0, 'added': 0}
    notable_rewrites = []

    for tag, fi, fj, sim in aligned:
        if tag == 'equal' or (tag == 'replace' and sim >= 0.9):
            changes['preserved'] += 1
        elif tag == 'replace':
            label = classify_sentence_pair(
                first_sents[fi] if fi is not None else '',
                final_sents[fj] if fj is not None else '',
                sim
            )
            if label == 'light_edit':
                changes['light_edit'] += 1
            else:
                changes['substantial_rewrite'] += 1
                if fi is not None and fj is not None:
                    notable_rewrites.append({
                        'first_sent': first_sents[fi][:120],
                        'final_sent': final_sents[fj][:120],
                        'similarity': round(sim, 3),
                    })
        elif tag == 'delete':
            changes['deleted'] += 1
        elif tag == 'insert':
            changes['added'] += 1

    # Sort notable rewrites by lowest similarity (most changed first)
    notable_rewrites.sort(key=lambda x: x['similarity'])
    notable_rewrites = notable_rewrites[:5]

    total_first = len(first_sents)
    substantially_changed = changes['substantial_rewrite'] + changes['deleted']
    change_rate = (substantially_changed / total_first * 100) if total_first > 0 else 0.0

    para_moves = detect_paragraph_moves(first_paras, final_paras)

    # Structural vs local: structural if paragraph moves are significant
    structural = len(para_moves) >= 2 or (len(para_moves) >= 1 and change_rate > 40)
    structural_vs_local = 'structural' if structural else 'local'

    return {
        'sentence_changes': changes,
        'change_rate': round(change_rate, 1),
        'paragraph_moves': para_moves,
        'notable_rewrites': notable_rewrites,
        'structural_vs_local': structural_vs_local,
        'total_first_sentences': total_first,
        'total_final_sentences': len(final_sents),
        'first_paragraph_count': len(first_paras),
        'final_paragraph_count': len(final_paras),
    }


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

SEP = '═' * 51


def format_diff_report(diff: dict) -> str:
    lines = []
    lines.append(f'\n{SEP}')
    lines.append('  DIFF ANALYSIS')
    lines.append(SEP)

    sc = diff['sentence_changes']
    total_first = diff['total_first_sentences']
    total_final = diff['total_final_sentences']

    lines.append(f'\n  Sentences: {total_first} → {total_final}')
    lines.append(f'  Paragraphs: {diff["first_paragraph_count"]} → {diff["final_paragraph_count"]}')
    lines.append(f'  Change rate: {diff["change_rate"]}% of first-draft sentences substantially changed/deleted')
    lines.append(f'  Pattern: {diff["structural_vs_local"].upper()} ({"para moves dominate" if diff["structural_vs_local"] == "structural" else "sentence-level edits dominate"})')

    lines.append('\n  Sentence breakdown:')
    lines.append(f'    Preserved:          {sc["preserved"]}')
    lines.append(f'    Light edits:        {sc["light_edit"]}')
    lines.append(f'    Substantial rewrites: {sc["substantial_rewrite"]}')
    lines.append(f'    Deleted:            {sc["deleted"]}')
    lines.append(f'    Added (new):        {sc["added"]}')

    if diff['paragraph_moves']:
        lines.append('\n  Paragraph moves detected:')
        for m in diff['paragraph_moves']:
            lines.append(f'    Para {m["first_position"]} → {m["final_position"]} (sim {m["similarity"]}): "{m["preview"]}"')
    else:
        lines.append('\n  No significant paragraph reordering detected.')

    if diff['notable_rewrites']:
        lines.append('\n  Most-changed sentences (lowest similarity first):')
        for i, r in enumerate(diff['notable_rewrites'], 1):
            lines.append(f'    [{i}] sim={r["similarity"]}')
            lines.append(f'        FIRST: {r["first_sent"]}')
            lines.append(f'        FINAL: {r["final_sent"]}')

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Standalone script entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) != 3:
        print(f'Usage: python3 {sys.argv[0]} FIRST_DRAFT FINAL_DRAFT', file=sys.stderr)
        sys.exit(1)
    first_path, final_path = sys.argv[1], sys.argv[2]
    try:
        with open(first_path) as f:
            first_text = f.read()
        with open(final_path) as f:
            final_text = f.read()
    except FileNotFoundError as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)
    diff = compute_diff(first_text, final_text)
    print(format_diff_report(diff))


if __name__ == '__main__':
    main()
