#!/usr/bin/env python3
"""
genre_separation.py — Genre/voice stylometric decomposition for voice-check.

Separates revision shifts (first → final draft) into two orthogonal components:
  - genre_component: shift along the (genre_centroid - user_centroid) direction.
    These are register adaptations toward the genre's expected style. They
    update the genre's stylometry centroid, NOT the user-level baseline.
  - voice_component: residual orthogonal to that direction. These are
    genre-agnostic compression / clarity moves that hold across genres. They
    update the user-level stylometry centroid.

The decomposition prevents genre adaptation (e.g., shorter sentences for
grant reviewers) from being mis-recorded as drift away from the user's voice.

Geometry, per the spec:
    For scalar metrics (sentence_distribution.mean, punctuation_ratios.*,
    vocabulary_richness.*):
        d = genre_value - user_value
        if abs(d) > epsilon:
            shift = final_value - first_value
            scalar_proj = shift / d              # how much of shift is along d
            scalar_proj = clamp(scalar_proj, 0, 1)
            genre_part = scalar_proj * d
            voice_part = shift - genre_part
        else:
            voice_part = shift; genre_part = 0

    For function-word centroid_z (50-dim vector):
        d = genre_centroid_z - user_centroid_z
        shift = final_z - first_z
        if dot(d, d) > epsilon:
            scalar_proj = dot(shift, d) / dot(d, d)
            scalar_proj = clamp(scalar_proj, 0, 1)
            genre_part = scalar_proj * d
            voice_part = shift - genre_part

EMA updates:
    target = current_centroid_value + component
    new = alpha * target + (1 - alpha) * current

Numpy is optional. Vector math falls back to list comprehensions when numpy
isn't importable.
"""

import copy
import sys
from collections import Counter

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


_EPS_SCALAR = 1e-9
_EPS_VECTOR = 1e-12


# ---------------------------------------------------------------------------
# Helpers: scalar projection and centroid_z extraction
# ---------------------------------------------------------------------------

def _scalar_decompose(user_val: float, genre_val: float,
                      first_val: float, final_val: float) -> tuple:
    """Decompose a scalar shift into (genre_part, voice_part).

    See module docstring for geometry. Returns (0.0, shift) when the genre
    direction is degenerate (genre_val ~= user_val).
    """
    shift = float(final_val) - float(first_val)
    d = float(genre_val) - float(user_val)
    if abs(d) <= _EPS_SCALAR:
        return 0.0, shift
    scalar_proj = shift / d
    if scalar_proj < 0.0:
        scalar_proj = 0.0
    elif scalar_proj > 1.0:
        scalar_proj = 1.0
    genre_part = scalar_proj * d
    voice_part = shift - genre_part
    return genre_part, voice_part


def _word_freq_to_z(word_freqs: dict, function_words: list,
                    corpus_mean: dict, corpus_stdev: dict) -> dict:
    """Project a word_freqs dict onto the function-word z-score space.

    Uses the user-level corpus_mean/corpus_stdev as the reference frame so
    user, genre, first, and final z-vectors live in the same coordinate system.
    """
    z = {}
    for fw in function_words:
        freq = float(word_freqs.get(fw, 0.0))
        mean = float(corpus_mean.get(fw, 0.0))
        stdev = float(corpus_stdev.get(fw, 1e-10))
        if stdev <= 0:
            stdev = 1e-10
        z[fw] = (freq - mean) / stdev
    return z


def _vector_decompose(user_z: dict, genre_z: dict,
                      first_z: dict, final_z: dict,
                      function_words: list) -> tuple:
    """Project the centroid_z shift onto the (genre - user) direction.

    Returns (genre_component_dict, voice_component_dict, scalar_proj).
    Each component dict maps function_word -> additive z-shift.
    """
    # Build aligned lists for vector math (numpy optional)
    d_list = [float(genre_z.get(fw, 0.0)) - float(user_z.get(fw, 0.0))
              for fw in function_words]
    shift_list = [float(final_z.get(fw, 0.0)) - float(first_z.get(fw, 0.0))
                  for fw in function_words]

    if NUMPY_AVAILABLE:
        d = np.array(d_list, dtype=float)
        shift = np.array(shift_list, dtype=float)
        d_dot_d = float(np.dot(d, d))
        if d_dot_d <= _EPS_VECTOR:
            genre_arr = np.zeros_like(shift)
            voice_arr = shift
            scalar_proj = 0.0
        else:
            scalar_proj = float(np.dot(shift, d)) / d_dot_d
            if scalar_proj < 0.0:
                scalar_proj = 0.0
            elif scalar_proj > 1.0:
                scalar_proj = 1.0
            genre_arr = scalar_proj * d
            voice_arr = shift - genre_arr
        genre_part = {fw: float(genre_arr[i]) for i, fw in enumerate(function_words)}
        voice_part = {fw: float(voice_arr[i]) for i, fw in enumerate(function_words)}
        return genre_part, voice_part, scalar_proj

    # Pure-Python fallback
    d_dot_d = sum(x * x for x in d_list)
    if d_dot_d <= _EPS_VECTOR:
        genre_part = {fw: 0.0 for fw in function_words}
        voice_part = {fw: shift_list[i] for i, fw in enumerate(function_words)}
        return genre_part, voice_part, 0.0
    shift_dot_d = sum(shift_list[i] * d_list[i] for i in range(len(function_words)))
    scalar_proj = shift_dot_d / d_dot_d
    if scalar_proj < 0.0:
        scalar_proj = 0.0
    elif scalar_proj > 1.0:
        scalar_proj = 1.0
    genre_part = {fw: scalar_proj * d_list[i] for i, fw in enumerate(function_words)}
    voice_part = {fw: shift_list[i] - genre_part[fw] for i, fw in enumerate(function_words)}
    return genre_part, voice_part, scalar_proj


# ---------------------------------------------------------------------------
# Public: decompose_stylometric_shift
# ---------------------------------------------------------------------------

# Scalar metrics decomposed individually. Each entry is (path_in_centroid, label).
# path is a tuple of nested keys; label is a human-readable description used in
# the report.
_SCALAR_PATHS = [
    (("sentence_distribution", "mean"), "Mean sentence length"),
    (("sentence_distribution", "stdev"), "Sentence length variability"),
    (("sentence_distribution", "skew"), "Sentence length skew"),
    (("punctuation_ratios", "semicolon"), "Semicolons/sentence"),
    (("punctuation_ratios", "colon"), "Colons/sentence"),
    (("punctuation_ratios", "paren"), "Parentheses/sentence"),
    (("punctuation_ratios", "question"), "Question marks/sentence"),
    (("punctuation_ratios", "emdash"), "Em-dashes/sentence"),
    (("vocabulary_richness", "ttr"), "Type-token ratio"),
    (("vocabulary_richness", "mattr"), "Moving-avg TTR"),
    (("vocabulary_richness", "yules_k"), "Yule's K"),
]

# Stylometry from compute_stylometry() puts these top-level. Pull values via path.
def _get_scalar(stylo: dict, path: tuple) -> float:
    cur = stylo
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return 0.0
        cur = cur[k]
    try:
        return float(cur)
    except (TypeError, ValueError):
        return 0.0


def _path_to_name(path: tuple) -> str:
    return ".".join(path)


def decompose_stylometric_shift(
    user_centroid: dict,
    genre_centroid: dict,
    first_stylo: dict,
    final_stylo: dict,
) -> dict:
    """Decompose the revision shift into genre-adaptive and voice components.

    Args:
        user_centroid: profile["stylometry"] — the user-level baseline.
        genre_centroid: profile["genres"][G]["stylometry"] — the genre baseline.
        first_stylo: compute_stylometry(first_text)
        final_stylo: compute_stylometry(final_text)

    Returns:
        {
            "genre_components": {
                "<scalar_name>": float,             # additive shift toward genre
                "centroid_z": {fw: float, ...},     # vector: per-function-word z-shift
                "centroid_z_scalar_proj": float,    # 0..1 fraction of shift along d
            },
            "voice_components": {
                "<scalar_name>": float,             # additive residual shift
                "centroid_z": {fw: float, ...},
            },
            "details": [
                {
                    "metric": str,
                    "path": tuple,
                    "user": float, "genre": float,
                    "first": float, "final": float,
                    "shift": float,
                    "genre_part": float, "voice_part": float,
                    "dominant": "genre" | "voice" | "neither",
                },
                ...
            ],
            "summary": {
                "genre_dominant_metrics": [str, ...],
                "voice_dominant_metrics": [str, ...],
                "interpretation": str,
            },
        }
    """
    genre_components: dict = {}
    voice_components: dict = {}
    details = []
    genre_dominant = []
    voice_dominant = []

    # ------- scalar metrics -------
    for path, label in _SCALAR_PATHS:
        user_v = _get_scalar(user_centroid, path)
        genre_v = _get_scalar(genre_centroid, path)
        first_v = _get_scalar(first_stylo, path)
        final_v = _get_scalar(final_stylo, path)
        genre_part, voice_part = _scalar_decompose(user_v, genre_v, first_v, final_v)
        shift = final_v - first_v

        name = _path_to_name(path)
        genre_components[name] = genre_part
        voice_components[name] = voice_part

        # Dominance: which component carries more of the shift magnitude?
        # Only meaningful when the shift itself is non-trivial.
        ag = abs(genre_part)
        av = abs(voice_part)
        if ag + av < _EPS_SCALAR:
            dominant = "neither"
        elif ag >= 2 * av:
            dominant = "genre"
            genre_dominant.append(label)
        elif av >= 2 * ag:
            dominant = "voice"
            voice_dominant.append(label)
        else:
            dominant = "neither"

        details.append({
            "metric": label,
            "path": path,
            "user": user_v,
            "genre": genre_v,
            "first": first_v,
            "final": final_v,
            "shift": shift,
            "genre_part": genre_part,
            "voice_part": voice_part,
            "dominant": dominant,
        })

    # ------- centroid_z vector -------
    function_words = list(user_centroid.get("function_words") or
                          genre_centroid.get("function_words") or [])
    corpus_mean = user_centroid.get("corpus_mean", {})
    corpus_stdev = user_centroid.get("corpus_stdev", {})

    user_z = dict(user_centroid.get("centroid_z", {}))
    genre_z = dict(genre_centroid.get("centroid_z", {}))

    # Project first/final word_freqs into the user's z-coordinate frame
    first_z = _word_freq_to_z(
        first_stylo.get("word_freqs", {}), function_words, corpus_mean, corpus_stdev
    )
    final_z = _word_freq_to_z(
        final_stylo.get("word_freqs", {}), function_words, corpus_mean, corpus_stdev
    )

    if function_words:
        z_genre_part, z_voice_part, z_scalar_proj = _vector_decompose(
            user_z, genre_z, first_z, final_z, function_words
        )
    else:
        z_genre_part, z_voice_part, z_scalar_proj = {}, {}, 0.0

    genre_components["centroid_z"] = z_genre_part
    genre_components["centroid_z_scalar_proj"] = z_scalar_proj
    voice_components["centroid_z"] = z_voice_part

    # Interpretation summary
    if not genre_dominant and not voice_dominant:
        interp = (
            "No metric showed a clearly genre- or voice-dominant shift. The "
            "revision moved within the threshold noise floor."
        )
    elif genre_dominant and not voice_dominant:
        interp = (
            f"Revision was primarily genre-adaptive: shifts in "
            f"{len(genre_dominant)} metric(s) projected onto the "
            f"(genre - user) direction. Genre centroid will absorb these; "
            f"user centroid is left effectively untouched."
        )
    elif voice_dominant and not genre_dominant:
        interp = (
            f"Revision was primarily a voice move: shifts in "
            f"{len(voice_dominant)} metric(s) were orthogonal to genre "
            f"adaptation. User centroid will incorporate these as voice signal."
        )
    else:
        interp = (
            f"Mixed revision: {len(genre_dominant)} metric(s) genre-adaptive, "
            f"{len(voice_dominant)} metric(s) voice-driven. Both centroids "
            f"will update on their respective components."
        )

    return {
        "genre_components": genre_components,
        "voice_components": voice_components,
        "details": details,
        "summary": {
            "genre_dominant_metrics": genre_dominant,
            "voice_dominant_metrics": voice_dominant,
            "interpretation": interp,
        },
    }


# ---------------------------------------------------------------------------
# EMA updates: genre and user centroids
# ---------------------------------------------------------------------------

def _set_scalar(centroid: dict, path: tuple, value: float):
    """Set a nested scalar value, creating intermediate dicts as needed."""
    cur = centroid
    for k in path[:-1]:
        if k not in cur or not isinstance(cur[k], dict):
            cur[k] = {}
        cur = cur[k]
    cur[path[-1]] = value


def _apply_scalar_ema(centroid: dict, components: dict, alpha: float, paths) -> dict:
    """For each scalar path, target = current + component; new = a*target + (1-a)*current."""
    out = copy.deepcopy(centroid)
    for path, _label in paths:
        name = _path_to_name(path)
        if name not in components:
            continue
        component = float(components[name])
        current = _get_scalar(out, path)
        target = current + component
        new_val = alpha * target + (1.0 - alpha) * current
        _set_scalar(out, path, round(new_val, 6))
    return out


def _apply_centroid_z_ema(centroid: dict, z_component: dict, alpha: float) -> dict:
    """EMA the function-word centroid_z dict by additive component."""
    out = copy.deepcopy(centroid)
    z = dict(out.get("centroid_z", {}))
    function_words = out.get("function_words", []) or list(z.keys())
    for fw in function_words:
        component = float(z_component.get(fw, 0.0))
        current = float(z.get(fw, 0.0))
        target = current + component
        new_val = alpha * target + (1.0 - alpha) * current
        z[fw] = round(new_val, 6)
    out["centroid_z"] = z
    return out


def update_genre_centroid_via_ema(genre_centroid: dict,
                                  genre_components: dict,
                                  alpha: float) -> dict:
    """Apply EMA to genre centroid using genre-direction components only.

    Returns a new dict (does not mutate input). Does NOT increment
    revision_count — caller manages counts so user-vs-genre revision counts
    can diverge cleanly.
    """
    out = _apply_scalar_ema(genre_centroid, genre_components, alpha, _SCALAR_PATHS)
    z_component = genre_components.get("centroid_z", {})
    if z_component:
        out = _apply_centroid_z_ema(out, z_component, alpha)
    return out


def update_user_centroid_via_ema_voice_only(user_centroid: dict,
                                            voice_components: dict,
                                            alpha: float) -> dict:
    """Apply EMA to user centroid using only the voice-residual components.

    Mirrors update_genre_centroid_via_ema but on the orthogonal residual.
    Returns a new dict; does not increment revision_count.
    """
    out = _apply_scalar_ema(user_centroid, voice_components, alpha, _SCALAR_PATHS)
    z_component = voice_components.get("centroid_z", {})
    if z_component:
        out = _apply_centroid_z_ema(out, z_component, alpha)
    return out


# ---------------------------------------------------------------------------
# Bootstrap: seed a genre centroid from a single revised draft
# ---------------------------------------------------------------------------

def seed_genre_centroid_from_stylometry(stylo: dict,
                                        calibration_sentence_count: int = None) -> dict:
    """Build a fresh genre stylometry dict from a single text's metrics.

    Used the first time --learn --genre X is called and no prior genre
    centroid exists. Mirrors the structure of profile['stylometry'] so
    later --learn calls can decompose against it.

    The function-word list, corpus_mean, and corpus_stdev are seeded from
    the single text's word_freqs. A genre centroid bootstrapped this way
    is roughly equivalent to a one-sample calibration: revision_count = 1,
    and subsequent --learn calls refine it via EMA.

    Args:
        stylo: output of compute_stylometry(text) for the seed text.
        calibration_sentence_count: optional sentence count override
            (defaults to stylo['sentence_count'] if available).

    Returns a dict matching the stylometry block schema.
    """
    word_freqs = dict(stylo.get("word_freqs") or {})
    # Top 50 by frequency in this text become the genre's function_word list.
    # If the seed text has fewer than 50 distinct frequent tokens, we use all.
    top = sorted(word_freqs.items(), key=lambda kv: kv[1], reverse=True)[:50]
    function_words = [w for w, _ in top]

    # corpus_mean = the seed text's relative frequencies.
    # corpus_stdev = a small floor (single-sample stdev is undefined). Using
    # mean/2 (with a small floor) gives downstream z-scores reasonable scale
    # without dividing by zero. Subsequent EMA updates will adjust.
    corpus_mean = {fw: float(word_freqs.get(fw, 0.0)) for fw in function_words}
    corpus_stdev = {
        fw: max(corpus_mean[fw] / 2.0, 1e-6) for fw in function_words
    }
    # centroid_z is zero by construction (z of the only sample relative to itself)
    centroid_z = {fw: 0.0 for fw in function_words}

    punct = dict(stylo.get("punctuation_ratios") or {})
    vocab = dict(stylo.get("vocabulary_richness") or {})
    sent = dict(stylo.get("sentence_distribution") or {})
    # Default missing keys to 0.0 so downstream code finds expected shape.
    for k in ("semicolon", "colon", "paren", "question", "emdash"):
        punct.setdefault(k, 0.0)
    for k in ("ttr", "mattr", "yules_k"):
        vocab.setdefault(k, 0.0)
    for k in ("mean", "stdev", "skew"):
        sent.setdefault(k, 0.0)

    word_count = int(stylo.get("word_count") or 0)
    sentence_count = (calibration_sentence_count
                      if calibration_sentence_count is not None
                      else int(stylo.get("sentence_count") or 0))

    seeded = {
        "function_words": function_words,
        "corpus_mean": corpus_mean,
        "corpus_stdev": corpus_stdev,
        "centroid_z": centroid_z,
        "punctuation_ratios": {k: round(float(v), 6) for k, v in punct.items()},
        "vocabulary_richness": {k: round(float(v), 6) for k, v in vocab.items()},
        "sentence_distribution": {k: round(float(v), 6) for k, v in sent.items()},
        # Distance threshold: with a single sample we have no intra-author
        # spread to measure. Use a loose default (1.5x base) — refined via
        # EMA as more revisions accumulate.
        "distance_threshold": 1.5,
        "intra_author_max_delta": None,
        "calibration_word_count": word_count,
        "style_notes": (
            f"Genre centroid seeded from a single revised draft "
            f"({word_count} words, {sentence_count} sentences). "
            f"Refines via EMA on subsequent --learn --genre calls."
        ),
        "revision_count": 1,
        "_seeded_from_single_sample": True,
    }
    return seeded


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------

def format_decomposition_report(decomp: dict, genre_name: str) -> str:
    """Format the two-section stylometry report (genre-adaptive vs. voice).

    Returns a multi-line string ready to print under a 'STYLOMETRY' header.
    Matches the format described in the spec — two clearly labeled sections
    with per-metric lines showing first → final → genre baseline drift.
    """
    lines = []
    lines.append(f"  STYLOMETRY (decomposed by --genre {genre_name})")
    lines.append("")

    # Genre-adaptive section
    genre_lines = []
    voice_lines = []
    near_zero_lines = []  # both parts very small — informational

    for d in decomp["details"]:
        # Skip when the shift itself is essentially zero
        if abs(d["shift"]) < _EPS_SCALAR and abs(d["genre_part"]) < _EPS_SCALAR \
                and abs(d["voice_part"]) < _EPS_SCALAR:
            continue
        line = (
            f"    {d['metric']}: {d['first']:.3f} → {d['final']:.3f} "
            f"(genre baseline {d['genre']:.3f}, user baseline {d['user']:.3f}); "
            f"shift {d['shift']:+.3f} = genre {d['genre_part']:+.3f} + voice {d['voice_part']:+.3f}"
        )
        if d["dominant"] == "genre":
            genre_lines.append(line)
        elif d["dominant"] == "voice":
            voice_lines.append(line)
        else:
            near_zero_lines.append(line)

    lines.append("  GENRE-ADAPTIVE SHIFTS (toward the genre register, updating genre centroid):")
    if genre_lines:
        lines.extend(genre_lines)
    else:
        lines.append("    (none — no metric shifted clearly along the genre direction)")
    lines.append("")

    lines.append("  VOICE SHIFTS (orthogonal residual, updating user centroid):")
    if voice_lines:
        lines.extend(voice_lines)
    else:
        lines.append("    (none — no metric shifted clearly orthogonal to the genre direction)")
    lines.append("")

    if near_zero_lines:
        lines.append("  MIXED / NEAR-NOISE (neither component clearly dominant):")
        lines.extend(near_zero_lines)
        lines.append("")

    # Function-word centroid_z summary line
    z_proj = decomp["genre_components"].get("centroid_z_scalar_proj", 0.0)
    lines.append(
        f"  Function-word centroid_z shift projection onto (genre - user): "
        f"{z_proj:.3f} (0 = pure voice move; 1 = pure genre adaptation)."
    )
    lines.append("")
    lines.append(f"  Interpretation: {decomp['summary']['interpretation']}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI / smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Minimal smoke test: build two fake centroids and decompose a shift.
    user_c = {
        "function_words": ["the", "and", "of"],
        "corpus_mean": {"the": 0.05, "and": 0.03, "of": 0.025},
        "corpus_stdev": {"the": 0.005, "and": 0.005, "of": 0.005},
        "centroid_z": {"the": 0.0, "and": 0.0, "of": 0.0},
        "sentence_distribution": {"mean": 21.6, "stdev": 12.4, "skew": 2.1},
        "punctuation_ratios": {"semicolon": 0.05, "colon": 0.26, "paren": 0.19,
                               "question": 0.04, "emdash": 0.35},
        "vocabulary_richness": {"ttr": 0.5, "mattr": 0.84, "yules_k": 77.8},
    }
    genre_c = {
        "function_words": user_c["function_words"],
        "corpus_mean": user_c["corpus_mean"],
        "corpus_stdev": user_c["corpus_stdev"],
        "centroid_z": {"the": 0.2, "and": -0.1, "of": 0.0},
        "sentence_distribution": {"mean": 17.0, "stdev": 10.0, "skew": 1.5},
        "punctuation_ratios": {"semicolon": 0.04, "colon": 0.24, "paren": 0.15,
                               "question": 0.03, "emdash": 0.30},
        "vocabulary_richness": {"ttr": 0.32, "mattr": 0.78, "yules_k": 55.0},
    }
    first_s = {
        "word_freqs": {"the": 0.05, "and": 0.03, "of": 0.025},
        "punctuation_ratios": {"semicolon": 0.05, "colon": 0.27, "paren": 0.20,
                               "question": 0.04, "emdash": 0.36},
        "vocabulary_richness": {"ttr": 0.30, "mattr": 0.80, "yules_k": 58.0},
        "sentence_distribution": {"mean": 19.1, "stdev": 18.1, "skew": 1.8},
        "word_count": 5482, "sentence_count": 287,
    }
    final_s = {
        "word_freqs": {"the": 0.054, "and": 0.029, "of": 0.025},
        "punctuation_ratios": {"semicolon": 0.045, "colon": 0.24, "paren": 0.18,
                               "question": 0.035, "emdash": 0.33},
        "vocabulary_richness": {"ttr": 0.32, "mattr": 0.79, "yules_k": 54.3},
        "sentence_distribution": {"mean": 17.3, "stdev": 16.5, "skew": 1.6},
        "word_count": 4585, "sentence_count": 265,
    }
    decomp = decompose_stylometric_shift(user_c, genre_c, first_s, final_s)
    print(format_decomposition_report(decomp, "grant_application"))
    print()
    print("genre-dominant metrics:", decomp["summary"]["genre_dominant_metrics"])
    print("voice-dominant metrics:", decomp["summary"]["voice_dominant_metrics"])
