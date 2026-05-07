#!/usr/bin/env python3
"""
writing_check.py — Quantitative voicing analysis for draft documents.

Measures sentence structure, em-dash usage, hedge words, self-aggrandizing frames,
topic sentence patterns, passive voice, cohesion markers, readability, narrative
padding, and product-description appositives against configurable thresholds.

Supports voice profiles: load patterns and thresholds from a JSON file so
different writers can use the tool with their own calibration.

Usage:
    python3 writing_check.py path/to/draft.md [--target 1200] [--json]
    python3 writing_check.py path/to/draft.md --profile path/to/profile.json
    python3 writing_check.py --calibrate path/to/samples/ [-o profile.json]

Dependencies (all pre-installed): textstat, nltk, re, json, sys
"""

import re
import sys
import json
import argparse
import os
from datetime import datetime

# Ensure script's directory is on sys.path so sibling modules (stylometry,
# perplexity, embeddings, diff_analysis) import reliably regardless of cwd
# or how Python is invoked.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import textstat
import nltk

# Ensure punkt tokenizer is available
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)
try:
    nltk.data.find("taggers/averaged_perceptron_tagger_eng")
except LookupError:
    nltk.download("averaged_perceptron_tagger_eng", quiet=True)

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag


# ---------------------------------------------------------------------------
# Configuration: patterns and thresholds
# ---------------------------------------------------------------------------

HEDGE_WORDS = [
    r"\bsuggests?\b",
    r"\bsuggesting\b",
    r"\bperhaps\b",
    r"\bpotentially\b",
    r"(?<![A-Z])\bmay\b(?!\s+\d)",  # exclude "May" (month) — capitalized or before a number
    r"\bmight\b",
    r"\bcould be\b",
    r"\bappears to\b",
    r"\bseems to\b",
]

SELF_AGGRANDIZING = [
    r"\bmost striking\b",
    r"\bmost interesting\b",
    r"\bmost important\b",
    r"\bgroundbreaking\b",
    r"\bparadigm\b",
    r"\btransformative\b",
    r"\bunprecedented\b",
    r"\bmost significant\b",
    r"\bmost compelling\b",
]

TOPIC_SENTENCE_STARTERS = [
    r"(?:^|\.\s+)This is\b",
    r"(?:^|\.\s+)These are\b",
    r"(?:^|\.\s+)That is\b",
]

LOGICAL_CONNECTORS = [
    r"\bhowever\b",
    r"\bmoreover\b",
    r"\bfurthermore\b",
    r"\badditionally\b",
    r"\bconsequently\b",
]

NARRATIVE_PADDING = [
    r"\bwhat happened next\b",
    r"\bwhat happened was\b",
    r"\bthis insight came from\b",
    r"\bit is worth noting\b",
    r"\bit should be noted\b",
    r"\bwhat draws me\b",
]

CORPORATE_JARGON = [
    r"\bactionable insights?\b",
    r"\bsurfacing needs\b",
    r"\btranslating findings\b",
    r"\bleveraging\b",
    r"\bstakeholder engagement\b",
    r"\bI(?:'d| would) welcome the chance\b",
    r"\bI am excited to\b",
    r"\bI am passionate about\b",
    r"\bthought leader(?:ship)?\b",
    r"\bsynerg(?:y|ies|istic)\b",
    r"\bparadigm shift\b",
    r"\bbest practices\b",
    r"\bkey takeaway\b",
    r"\bimpactful\b",
    r"\binnovative solutions?\b",
    r"\bscalable\b",
]

# Thresholds (from VOICING_PARAMETERS.md)
THRESH_LONG_SENT = 40
THRESH_REWRITE_SENT = 50
THRESH_LONG_SENT_MAX = 4
THRESH_REWRITE_SENT_MAX = 2
THRESH_EMDASH_PER_1000 = 15
THRESH_EMDASH_INSERT_WORDS = 10
THRESH_HEDGE_MAX = 0
THRESH_AGGRANDIZE_MAX = 0
THRESH_TOPIC_THIS_MAX = 2
THRESH_CONNECTOR_MAX = 3
THRESH_PADDING_MAX = 0
THRESH_PRODUCT_MAX = 0
THRESH_JARGON_MAX = 0
THRESH_WORDCOUNT_OVER = 1.10  # 110% of target

# How many consecutive learn runs a diagnostic check can be absent from cited
# checks before surfacing in the DIAGNOSTIC REVIEW DUE block.
DIAGNOSTIC_SILENCE_THRESHOLD = 5

# Paths for persistent learning-loop tracking files.
CITATION_LOG_PATH = os.path.join(_SCRIPT_DIR, "citation_log.json")
PROFILE_CHANGE_LOG_PATH = os.path.join(_SCRIPT_DIR, "PROFILE_CHANGE_LOG.md")

# ---------------------------------------------------------------------------
# Phase 4 qualitative prompt — shared by --learn and --learn-sequence
# ---------------------------------------------------------------------------

PHASE_4_PROFILE_ACTIONS = """
  PROFILE ACTIONS
  □ **Editorial discipline: the profile should sharpen with each loop, not grow. Treat addition as the option of last resort, after rephrase and merge are ruled out.**
  □ Map each major change type to existing qualitative checks. Which checks predicted the change? (signals they're working.)
  □ What is the smallest set of profile changes — additions, deletions, merges, or rephrasings — that would have caught the deliberate revision moves? Consider each lens:
      • REPHRASE: did an existing check fire weakly because its instruction is imprecise? Sharpen the language.
      • MERGE: did two or more checks point at the same concern from different angles? Collapse them, absorbing distinctive language.
      • ROLE-REASSIGN or CUT: was a check tagged `pre_draft` that didn't actually shape this revision? Demote to `diagnostic`, or cut.
      • ADD: is there a genuinely new pattern not covered? Specify role at insertion (pre_draft / linter / cda_sweep / diagnostic). If `pre_draft`, name what existing pre_draft check it replaces — the in-flight set is capped, additions force tradeoffs.
      • CUT (silence): are there checks that haven't fired across this or the last several revisions? Flag for next audit.
  □ For accepted additions and significant rephrasings, append an entry to `~/.claude/skills/voice-check/PROFILE_CHANGE_LOG.md`: source diff snippet (quoted, not summarized) + rationale + role + a question for the next audit. Merges and cuts don't require log entries (they reorganize existing rationale rather than create new). This preserves the *why* against rationale drift, separately from the citation log's tracking of *whether the check is still firing*.
  □ Present proposed changes to the user for approval before updating.
"""


# ---------------------------------------------------------------------------
# Profile loading and merging
# ---------------------------------------------------------------------------

def merge_profiles(base: dict, user: dict) -> dict:
    """Merge a base profile and a sparse user profile into a single effective profile.

    Merge semantics:
    - Patterns: base + user lists concatenated per category. User _disable dict removes
      exact-string matches from base. New user categories are added.
    - Thresholds: user values override base (sparse dict merge).
    - Qualitative: base checks first; user checks with same ID replace base check;
      user checks with new IDs are appended.
    - Genres, stylometry, perplexity, embeddings: from user only (base has none).
    - Profile metadata: from user profile.
    """
    merged = {}

    # Profile metadata: from user
    merged["profile"] = user.get("profile", base.get("profile", {}))

    # Patterns: extend per category, apply _disable
    base_patterns = base.get("patterns", {})
    user_patterns = {k: v for k, v in user.get("patterns", {}).items() if k != "_disable"}
    disable_map = user.get("patterns", {}).get("_disable", {})

    merged_patterns = {}
    all_categories = set(base_patterns.keys()) | set(user_patterns.keys())
    for cat in all_categories:
        combined = list(base_patterns.get(cat, [])) + list(user_patterns.get(cat, []))
        disabled = set(disable_map.get(cat, []))
        if disabled:
            combined = [p for p in combined if p not in disabled]
        merged_patterns[cat] = combined
    merged["patterns"] = merged_patterns

    # Thresholds: user overrides base
    merged["thresholds"] = {**base.get("thresholds", {}), **user.get("thresholds", {})}

    # Qualitative: base checks first, user overrides by ID or appends
    qual_by_id = {q["id"]: q for q in base.get("qualitative", [])}
    for q in user.get("qualitative", []):
        qual_by_id[q["id"]] = q  # replace or add
    merged["qualitative"] = list(qual_by_id.values())

    # Genres: from user only (base has none)
    if "genres" in user:
        merged["genres"] = user["genres"]

    # Computational linguistics: from user only
    for key in ("stylometry", "perplexity", "embeddings"):
        if key in user:
            merged[key] = user[key]

    return merged


def discover_profile():
    """Auto-discover user profile in the profiles directory.

    Returns (path, count) where:
    - path is the profile path if exactly one non-base profile found, None otherwise
    - count is the number of non-base profiles found
    """
    profiles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles")
    if not os.path.isdir(profiles_dir):
        return None, 0

    candidates = [
        f for f in os.listdir(profiles_dir)
        if f.endswith(".json") and f != "base.json"
    ]

    if len(candidates) == 1:
        return os.path.join(profiles_dir, candidates[0]), 1
    return None, len(candidates)


def load_profile(profile_path: str) -> dict:
    """Load a voice profile from JSON. Validates structure and regex patterns.

    If the profile has a "base" field, loads the base profile and merges them.
    Stashes _user_profile_path on the merged result so learn_from_revision knows
    where to write back. Backwards compatible: profiles without "base" are returned
    as-is.
    """
    try:
        with open(profile_path, "r", encoding="utf-8") as f:
            user = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Profile at {profile_path} is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate regex patterns compile correctly
    for category in ("hedge_words", "self_aggrandizing", "topic_sentence_starters",
                      "logical_connectors", "narrative_padding", "corporate_jargon"):
        for pattern_str in user.get("patterns", {}).get(category, []):
            try:
                re.compile(pattern_str, re.IGNORECASE)
            except re.error as e:
                print(f"Error: Invalid regex in profile patterns.{category}: "
                      f"\"{pattern_str}\" — {e}", file=sys.stderr)
                sys.exit(1)

    # If no base reference, return as standalone (backwards compatible)
    if "base" not in user:
        return user

    # Resolve base path relative to user profile's directory
    profile_dir = os.path.dirname(os.path.abspath(profile_path))
    base_path = os.path.join(profile_dir, user["base"])
    if not os.path.exists(base_path):
        print(f"Warning: Base profile not found at {base_path}. Using user profile standalone.",
              file=sys.stderr)
        return user

    try:
        with open(base_path, "r", encoding="utf-8") as f:
            base = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Warning: Base profile at {base_path} is not valid JSON: {e}. "
              f"Using user profile standalone.", file=sys.stderr)
        return user

    merged = merge_profiles(base, user)
    # Stash paths for learn-back writes
    merged["_user_profile_path"] = profile_path
    merged["_base_path"] = base_path
    return merged


def apply_profile(profile: dict, genre: str = None):
    """Override global patterns and thresholds from a loaded profile.

    If genre is specified and exists in profile['genres'], genre-specific
    threshold_overrides are merged on top of base thresholds (genre wins).

    Note: the profile's 'qualitative' and 'genres.*.qualitative' sections
    are not used by this script. They contain CDA checklist instructions
    consumed by the LLM running the /voice-check skill. This script handles
    quantitative analysis only.

    Returns the genre's word_count_target if available, else None.
    """
    global HEDGE_WORDS, SELF_AGGRANDIZING, TOPIC_SENTENCE_STARTERS
    global LOGICAL_CONNECTORS, NARRATIVE_PADDING, CORPORATE_JARGON
    global THRESH_LONG_SENT, THRESH_REWRITE_SENT, THRESH_LONG_SENT_MAX
    global THRESH_REWRITE_SENT_MAX, THRESH_EMDASH_PER_1000, THRESH_EMDASH_INSERT_WORDS
    global THRESH_HEDGE_MAX, THRESH_AGGRANDIZE_MAX, THRESH_TOPIC_THIS_MAX
    global THRESH_CONNECTOR_MAX, THRESH_PADDING_MAX, THRESH_PRODUCT_MAX
    global THRESH_JARGON_MAX, THRESH_WORDCOUNT_OVER

    patterns = profile.get("patterns", {})
    if "hedge_words" in patterns:
        HEDGE_WORDS = patterns["hedge_words"]
    if "self_aggrandizing" in patterns:
        SELF_AGGRANDIZING = patterns["self_aggrandizing"]
    if "topic_sentence_starters" in patterns:
        TOPIC_SENTENCE_STARTERS = patterns["topic_sentence_starters"]
    if "logical_connectors" in patterns:
        LOGICAL_CONNECTORS = patterns["logical_connectors"]
    if "narrative_padding" in patterns:
        NARRATIVE_PADDING = patterns["narrative_padding"]
    if "corporate_jargon" in patterns:
        CORPORATE_JARGON = patterns["corporate_jargon"]

    # Build merged thresholds: base from profile, then genre overrides on top
    thresholds = dict(profile.get("thresholds", {}))
    genre_word_count_target = None

    if genre and "genres" in profile:
        genre_config = profile["genres"].get(genre)
        if genre_config:
            genre_word_count_target = genre_config.get("word_count_target")
            genre_overrides = genre_config.get("threshold_overrides", {})
            thresholds.update(genre_overrides)

    if "long_sentence_words" in thresholds:
        THRESH_LONG_SENT = thresholds["long_sentence_words"]
    if "rewrite_sentence_words" in thresholds:
        THRESH_REWRITE_SENT = thresholds["rewrite_sentence_words"]
    if "long_sentence_max" in thresholds:
        THRESH_LONG_SENT_MAX = thresholds["long_sentence_max"]
    if "rewrite_sentence_max" in thresholds:
        THRESH_REWRITE_SENT_MAX = thresholds["rewrite_sentence_max"]
    if "emdash_per_1000w" in thresholds:
        THRESH_EMDASH_PER_1000 = thresholds["emdash_per_1000w"]
    if "emdash_insertion_words" in thresholds:
        THRESH_EMDASH_INSERT_WORDS = thresholds["emdash_insertion_words"]
    if "hedge_max" in thresholds:
        THRESH_HEDGE_MAX = thresholds["hedge_max"]
    if "self_aggrandizing_max" in thresholds:
        THRESH_AGGRANDIZE_MAX = thresholds["self_aggrandizing_max"]
    if "topic_opener_max" in thresholds:
        THRESH_TOPIC_THIS_MAX = thresholds["topic_opener_max"]
    if "logical_connector_max" in thresholds:
        THRESH_CONNECTOR_MAX = thresholds["logical_connector_max"]
    if "narrative_padding_max" in thresholds:
        THRESH_PADDING_MAX = thresholds["narrative_padding_max"]
    if "product_description_max" in thresholds:
        THRESH_PRODUCT_MAX = thresholds["product_description_max"]
    if "corporate_jargon_max" in thresholds:
        THRESH_JARGON_MAX = thresholds["corporate_jargon_max"]
    if "wordcount_over_pct" in thresholds:
        THRESH_WORDCOUNT_OVER = thresholds["wordcount_over_pct"] / 100.0

    return genre_word_count_target


# ---------------------------------------------------------------------------
# Calibration: analyze a corpus and generate a starter profile
# ---------------------------------------------------------------------------

def calibrate_from_samples(sample_dir: str, output_path: str = None,
                           genre: str = None):
    """
    Analyze a directory of writing samples and generate a voice profile
    with thresholds derived from the writer's actual patterns.

    Computes baseline frequencies for quantitative metrics, then sets
    thresholds at approximately 1.5 standard deviations above the mean
    (or at the observed maximum, whichever is higher).

    The qualitative section is left as a skeleton — the LLM fills it in
    by reading the samples and extracting voice characteristics.

    Genre-specific calibration:
        If `genre` is provided AND the output path resolves to an existing
        profile, the calibration is written into
        profile["genres"][genre]["stylometry"] (preserving the rest of the
        profile). The user-level stylometry block is NOT modified. This is
        how per-genre centroids are bootstrapped from a curated sample set
        (e.g., several revised grant drafts for genre='grant_application').
    """
    import glob
    import statistics

    # Find samples
    samples = []
    for ext in ("*.md", "*.txt", "*.html"):
        samples.extend(glob.glob(os.path.join(sample_dir, ext)))
        samples.extend(glob.glob(os.path.join(sample_dir, "**", ext), recursive=True))
    # Deduplicate preserving order
    seen = set()
    unique_samples = []
    for s in samples:
        real = os.path.realpath(s)
        if real not in seen:
            seen.add(real)
            unique_samples.append(s)
    samples = unique_samples

    if not samples:
        print(f"Error: No .md, .txt, or .html files found in {sample_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Calibrating from {len(samples)} writing sample(s)...")

    # Collect metrics across all samples
    all_sentence_lengths = []
    all_emdash_densities = []
    all_hedge_rates = []
    all_aggrandize_rates = []
    all_topic_opener_counts = []
    all_connector_rates = []
    all_padding_rates = []
    all_jargon_rates = []
    all_product_rates = []


    for sample_path in samples:
        print(f"  Analyzing: {os.path.basename(sample_path)}")
        results = run_analysis(sample_path, target=999999)  # no word count target for calibration

        if results.get("empty"):
            continue

        wc = results["words"]["total"]
        if wc < 50:
            continue

        # Sentence lengths
        sents = results["sentences"]
        if sents["count"] > 0:
            all_sentence_lengths.append(sents["max_length"])

        # Em-dash density
        all_emdash_densities.append(results["emdashes"]["per_1000"])

        # Rates per 1000 words
        rate = lambda count: (count / wc) * 1000 if wc > 0 else 0
        all_hedge_rates.append(rate(results["hedges"]["count"]))
        all_aggrandize_rates.append(rate(results["aggrandizing"]["count"]))
        all_topic_opener_counts.append(results["topic_sentences"]["count"])
        all_connector_rates.append(rate(results["connectors"]["count"]))
        all_padding_rates.append(rate(results["padding"]["count"]))
        all_jargon_rates.append(rate(results["corporate_jargon"]["count"]))
        all_product_rates.append(rate(results["product_descriptions"]["count"]))

    if not all_sentence_lengths:
        print("Error: No samples had enough content to analyze.", file=sys.stderr)
        sys.exit(1)

    # Compute thresholds: mean + 1.5 * stdev, with floor and ceiling
    def threshold(values, floor=0, ceiling=None, round_to=0):
        if not values:
            return floor
        mean = statistics.mean(values)
        stdev = statistics.stdev(values) if len(values) > 1 else mean * 0.2
        computed = mean + 1.5 * stdev
        result = max(computed, floor)
        if ceiling is not None:
            result = min(result, ceiling)
        return round(result, round_to) if round_to else int(round(result))

    # For counts, use the max observed + a small buffer
    def count_threshold(values, buffer=1, ceiling=None):
        if not values:
            return buffer
        result = int(max(values)) + buffer
        if ceiling is not None:
            result = min(result, ceiling)
        return result

    # Compute all thresholds from samples
    computed_thresholds = {
        "long_sentence_words": threshold(all_sentence_lengths, floor=35, ceiling=55),
        "rewrite_sentence_words": threshold(all_sentence_lengths, floor=45, ceiling=65) + 10,
        "long_sentence_max": 6,
        "rewrite_sentence_max": 3,
        "emdash_per_1000w": threshold(all_emdash_densities, floor=5, ceiling=25, round_to=1),
        "emdash_insertion_words": 12,
        "hedge_max": count_threshold(all_hedge_rates, buffer=1, ceiling=3) if statistics.mean(all_hedge_rates) > 0.5 else 0,
        "self_aggrandizing_max": 0,
        "topic_opener_max": count_threshold(all_topic_opener_counts, buffer=1, ceiling=5),
        "logical_connector_max": count_threshold(all_connector_rates, buffer=1, ceiling=6) if statistics.mean(all_connector_rates) > 1 else 3,
        "narrative_padding_max": 0,
        "product_description_max": 0,
        "corporate_jargon_max": 0,
        "wordcount_over_pct": 115
    }

    # Load base thresholds for sparse diff — only store overrides
    base_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles", "base.json")
    base_thresholds = {}
    has_base = os.path.exists(base_json_path)
    if has_base:
        try:
            with open(base_json_path, "r", encoding="utf-8") as f:
                base_thresholds = json.load(f).get("thresholds", {})
        except (json.JSONDecodeError, OSError):
            has_base = False

    # Build sparse thresholds: only include values that differ from base
    if has_base:
        sparse_thresholds = {
            k: v for k, v in computed_thresholds.items()
            if k not in base_thresholds or v != base_thresholds[k]
        }
    else:
        sparse_thresholds = computed_thresholds

    # Build profile — sparse format if base.json exists, full format otherwise
    profile = {
        "profile": {
            "name": "[Your Name]",
            "version": "1.0",
            "created": __import__("datetime").date.today().isoformat(),
            "calibrated_from": f"{len(samples)} writing sample(s) in {sample_dir}",
            "description": "Auto-calibrated voice profile. Edit name, description, and qualitative checks to match your voice."
        },
        "thresholds": sparse_thresholds,
        "patterns": {},  # empty — user adds personal anti-patterns during setup
        "qualitative": [],  # empty skeleton — agent fills during setup
        "_instructions": (
            "This profile was auto-generated from your writing samples. "
            "It uses a three-layer architecture: base.json (universal norms) + this file (your overrides) + genre (per-document overrides). "
            "To customize: (1) Edit 'profile.name' and 'profile.description'. "
            "(2) Add patterns specific to YOUR anti-patterns in the 'patterns' section (these extend the base patterns). "
            "(3) Use '/voice-check setup' to have the LLM analyze your samples and generate qualitative checks. "
            "(4) Use '/voice-check genre' to configure genres through a guided conversation. "
            "(5) Adjust thresholds after running the tool on a few drafts (only values that differ from base need to be listed)."
        )
    }

    if has_base:
        profile["base"] = "base.json"

    if output_path is None:
        output_path = os.path.join(sample_dir, "voice_profile.json")

    # Extend profile with stylometry fingerprint (requires numpy)
    try:
        from stylometry import calibrate_stylometry
        print("\n  Computing stylometry fingerprint...")
        stylo_data = calibrate_stylometry(samples, verbose=True)
        if stylo_data:
            profile["stylometry"] = stylo_data
            print(f"  Stylometry: {stylo_data.get('style_notes', '')[:120]}")
        else:
            print("  Stylometry: skipped (calibration returned no data).")
    except ImportError:
        print("  Stylometry: skipped (stylometry.py not found).", file=sys.stderr)

    # Extend profile with perplexity baseline (requires mlx_lm)
    try:
        from perplexity import calibrate_perplexity
        print("\n  Computing perplexity baseline...")
        ppl_data = calibrate_perplexity(samples, verbose=True)
        if ppl_data:
            profile["perplexity"] = ppl_data
            print(f"  Perplexity: {ppl_data.get('style_notes', '')[:120]}")
        else:
            print("  Perplexity: skipped (MLX not available or calibration returned no data).")
    except ImportError:
        print("  Perplexity: skipped (perplexity.py not found).", file=sys.stderr)

    # Extend profile with embedding centroid (requires fastembed)
    try:
        from embeddings import calibrate_embeddings
        print("\n  Computing embedding centroid...")
        emb_data = calibrate_embeddings(samples, verbose=True)
        if emb_data:
            profile["embeddings"] = emb_data
            print(f"  Embeddings: {emb_data.get('style_notes', '')[:120]}")
        else:
            print("  Embeddings: skipped (fastembed not available or calibration returned no data).")
    except ImportError:
        print("  Embeddings: skipped (embeddings.py not found).", file=sys.stderr)

    # Genre-mode calibration: merge the computed stylometry into an existing
    # profile under genres[genre].stylometry, leaving root stylometry alone.
    if genre:
        if not os.path.isfile(output_path):
            print(f"Error: --calibrate --genre requires --output (or default path) to "
                  f"point at an EXISTING user profile. Not found: {output_path}",
                  file=sys.stderr)
            sys.exit(1)
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"Error: Could not read existing profile at {output_path}: {e}",
                  file=sys.stderr)
            sys.exit(1)

        if "genres" not in existing or not isinstance(existing.get("genres"), dict):
            existing["genres"] = {}
        if genre not in existing["genres"] or not isinstance(existing["genres"][genre], dict):
            existing["genres"][genre] = {
                "description": f"Auto-created by --calibrate --genre {genre}",
            }

        # Build a stylometry block for the genre. Use the same structure as
        # root stylometry, sourced from the samples we just analyzed.
        genre_stylo = profile.get("stylometry")
        if genre_stylo is None:
            print(f"Error: stylometry calibration produced no data; cannot seed "
                  f"genre '{genre}'. Check sample directory for readable text.",
                  file=sys.stderr)
            sys.exit(1)
        # Stamp this as a genre centroid (so downstream code can treat it
        # differently from a single-sample bootstrap).
        genre_stylo = dict(genre_stylo)
        genre_stylo.setdefault("revision_count", 0)
        existing["genres"][genre]["stylometry"] = genre_stylo

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

        print(f"\n  Genre stylometry written to: {output_path}")
        print(f"  Wrote: profile.genres.{genre}.stylometry "
              f"(from {len(samples)} sample(s), {profile['stylometry'].get('calibration_word_count', 0)} words)")
        print(f"  Note: user-level stylometry NOT modified.")
        return

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

    print(f"\n  Profile written to: {output_path}")
    if has_base:
        print(f"  Profile format: sparse (references base.json; only {len(sparse_thresholds)} threshold override(s) stored)")
    print(f"\n  Computed thresholds from {len(samples)} sample(s):")
    t = computed_thresholds
    print(f"    Long sentence:    {t['long_sentence_words']} words")
    print(f"    Rewrite sentence: {t['rewrite_sentence_words']} words")
    print(f"    Em-dash density:  {t['emdash_per_1000w']}/1000 words")
    print(f"    Hedge tolerance:  {t['hedge_max']}")
    print(f"    Connector max:    {t['logical_connector_max']}")
    print(f"\n  Next steps:")
    print(f"    1. Edit the profile: set your name, description, and add your personal anti-patterns")
    print(f"    2. Run '/voice-check setup' to extract qualitative voice characteristics")
    print(f"    3. Use it: python3 writing_check.py draft.md --profile {output_path}")
    print()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def strip_markdown_formatting(text: str) -> str:
    """Remove markdown bold/italic markers for analysis, keep everything else."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    return text


def load_and_prepare(filepath: str):
    """
    Load a markdown file. Return:
      - raw_lines: original lines with line numbers (1-indexed)
      - analysis_text: text with headers stripped and markdown formatting removed
      - header_count: number of header lines stripped
    """
    with open(filepath, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    header_count = 0
    body_lines = []
    body_line_map = []  # maps body line index -> original 1-indexed line number

    for i, line in enumerate(raw_lines):
        if line.strip().startswith("#"):
            header_count += 1
        else:
            body_lines.append(line)
            body_line_map.append(i + 1)

    body_text = "".join(body_lines)
    analysis_text = strip_markdown_formatting(body_text)

    return raw_lines, analysis_text, body_lines, body_line_map, header_count


def find_line_number(raw_lines, pattern_match_text, start_search=0):
    """Find the 1-indexed line number containing a piece of text."""
    clean_fragment = strip_markdown_formatting(pattern_match_text.strip())[:60]
    for i in range(start_search, len(raw_lines)):
        clean_line = strip_markdown_formatting(raw_lines[i])
        if clean_fragment in clean_line:
            return i + 1
    return 0


def context_snippet(text: str, match_start: int, match_end: int, window: int = 40) -> str:
    """Extract a context window around a match position."""
    ctx_start = max(0, match_start - window)
    ctx_end = min(len(text), match_end + window)
    snippet = text[ctx_start:ctx_end].replace("\n", " ").strip()
    if ctx_start > 0:
        snippet = "..." + snippet
    if ctx_end < len(text):
        snippet = snippet + "..."
    return snippet


def get_line_for_position(body_lines, body_line_map, position: int) -> int:
    """Given a character position in the joined body text, return the original line number."""
    cumulative = 0
    for idx, line in enumerate(body_lines):
        cumulative += len(line)
        if position < cumulative:
            return body_line_map[idx]
    return body_line_map[-1] if body_line_map else 0


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def analyze_words(analysis_text: str, target: int):
    words = word_tokenize(analysis_text)
    word_count = len(words)
    pct_diff = ((word_count - target) / target) * 100 if target > 0 else 0
    over_target = word_count > target * THRESH_WORDCOUNT_OVER
    return {
        "total": word_count,
        "target": target,
        "pct_diff": round(pct_diff, 1),
        "flag": over_target,
    }


def analyze_sentences(analysis_text: str):
    sentences = sent_tokenize(analysis_text)
    lengths = []
    long_sentences = []  # (sentence, word_count, approx line)

    for sent in sentences:
        wc = len(word_tokenize(sent))
        lengths.append(wc)

    count = len(sentences)
    avg = round(sum(lengths) / count, 1) if count else 0
    max_len = max(lengths) if lengths else 0
    over_long = [(s, l) for s, l in zip(sentences, lengths) if l > THRESH_LONG_SENT]
    over_rewrite = [(s, l) for s, l in zip(sentences, lengths) if l > THRESH_REWRITE_SENT]

    return {
        "count": count,
        "avg_length": avg,
        "max_length": max_len,
        "long_threshold": THRESH_LONG_SENT,
        "rewrite_threshold": THRESH_REWRITE_SENT,
        "over_long_count": len(over_long),
        "over_rewrite_count": len(over_rewrite),
        "over_long": over_long,
        "over_rewrite": over_rewrite,
        "flag_long": len(over_long) > THRESH_LONG_SENT_MAX,
        "flag_rewrite": len(over_rewrite) > THRESH_REWRITE_SENT_MAX,
    }


def analyze_emdashes(analysis_text: str, word_count: int, raw_lines, body_lines, body_line_map):
    # Count all em-dashes (both unicode and double-hyphen)
    emdash_pattern = re.compile(r"[\u2014]|--")
    all_dashes = list(emdash_pattern.finditer(analysis_text))
    total = len(all_dashes)
    per_1000 = round((total / word_count) * 1000, 1) if word_count > 0 else 0

    # Find em-dash insertions (text between PAIRED em-dashes within a sentence).
    # Constraints: no newlines, no sentence-ending punctuation (. ? !) between
    # the pair, which prevents matching two independent em-dashes in different
    # sentences on the same line.
    insertion_pattern = re.compile(r"(?:[\u2014]|--)\s*([^\n.!?]+?)\s*(?:[\u2014]|--)")
    long_insertions = []

    for m in insertion_pattern.finditer(analysis_text):
        insertion_text = m.group(1)
        insertion_wc = len(word_tokenize(insertion_text))
        if insertion_wc > THRESH_EMDASH_INSERT_WORDS:
            line_no = get_line_for_position(body_lines, body_line_map, m.start())
            long_insertions.append({
                "line": line_no,
                "text": insertion_text.strip()[:80],
                "word_count": insertion_wc,
            })

    return {
        "total": total,
        "per_1000": per_1000,
        "long_insertions": long_insertions,
        "flag_density": per_1000 > THRESH_EMDASH_PER_1000,
        "flag_insertions": len(long_insertions) > 0,
    }


def analyze_hedges(analysis_text: str, raw_lines, body_lines, body_line_map):
    findings = []
    for pattern_str in HEDGE_WORDS:
        pat = re.compile(pattern_str, re.IGNORECASE)
        for m in pat.finditer(analysis_text):
            word = m.group()
            line_no = get_line_for_position(body_lines, body_line_map, m.start())
            ctx = context_snippet(analysis_text, m.start(), m.end())
            findings.append({
                "line": line_no,
                "word": word,
                "context": ctx,
            })
    return {
        "count": len(findings),
        "items": findings,
        "flag": len(findings) > THRESH_HEDGE_MAX,
    }


def analyze_aggrandizing(analysis_text: str, raw_lines, body_lines, body_line_map):
    findings = []
    for pattern_str in SELF_AGGRANDIZING:
        pat = re.compile(pattern_str, re.IGNORECASE)
        for m in pat.finditer(analysis_text):
            phrase = m.group()
            line_no = get_line_for_position(body_lines, body_line_map, m.start())
            ctx = context_snippet(analysis_text, m.start(), m.end())
            findings.append({
                "line": line_no,
                "phrase": phrase,
                "context": ctx,
            })
    return {
        "count": len(findings),
        "items": findings,
        "flag": len(findings) > THRESH_AGGRANDIZE_MAX,
    }


def analyze_topic_sentences(analysis_text: str, raw_lines, body_lines, body_line_map):
    findings = []
    for pattern_str in TOPIC_SENTENCE_STARTERS:
        pat = re.compile(pattern_str, re.IGNORECASE | re.MULTILINE)
        for m in pat.finditer(analysis_text):
            # grab the rest of the sentence
            end_match = re.search(r"[.!?]", analysis_text[m.end():])
            if end_match:
                sentence_end = m.end() + end_match.end()
            else:
                sentence_end = min(m.end() + 80, len(analysis_text))
            sentence_start_text = analysis_text[m.start():sentence_end].strip()
            # Clean up leading period+space if captured
            sentence_start_text = re.sub(r"^\.\s*", "", sentence_start_text)
            line_no = get_line_for_position(body_lines, body_line_map, m.start())
            findings.append({
                "line": line_no,
                "text": sentence_start_text[:100],
            })
    return {
        "count": len(findings),
        "items": findings,
        "flag": len(findings) > THRESH_TOPIC_THIS_MAX,
    }


def analyze_passive_voice(analysis_text: str):
    """
    Approximate passive voice detection: auxiliary (was/were/is/are/been/be/being)
    followed by a past participle (VBN tag).
    """
    sentences = sent_tokenize(analysis_text)
    passive_count = 0
    passive_examples = []

    aux_pattern = re.compile(
        r"\b(was|were|is|are|been|be|being)\s+(\w+)", re.IGNORECASE
    )

    for sent in sentences:
        for m in aux_pattern.finditer(sent):
            candidate = m.group(2)
            tagged = pos_tag([candidate])
            if tagged and tagged[0][1] == "VBN":
                passive_count += 1
                if len(passive_examples) < 5:
                    passive_examples.append(sent.strip()[:100])
                break  # count once per sentence

    return {
        "count": passive_count,
        "examples": passive_examples,
    }


def analyze_connectors(analysis_text: str, raw_lines, body_lines, body_line_map):
    findings = []
    for pattern_str in LOGICAL_CONNECTORS:
        pat = re.compile(pattern_str, re.IGNORECASE)
        for m in pat.finditer(analysis_text):
            word = m.group()
            line_no = get_line_for_position(body_lines, body_line_map, m.start())
            findings.append({
                "line": line_no,
                "word": word,
            })
    return {
        "count": len(findings),
        "items": findings,
        "flag": len(findings) > THRESH_CONNECTOR_MAX,
    }


def analyze_readability(analysis_text: str):
    fk = textstat.flesch_kincaid_grade(analysis_text)
    fog = textstat.gunning_fog(analysis_text)
    fre = textstat.flesch_reading_ease(analysis_text)
    return {
        "flesch_kincaid": round(fk, 1),
        "gunning_fog": round(fog, 1),
        "flesch_reading_ease": round(fre, 1),
    }


def analyze_padding(analysis_text: str, raw_lines, body_lines, body_line_map):
    findings = []
    for pattern_str in NARRATIVE_PADDING:
        pat = re.compile(pattern_str, re.IGNORECASE)
        for m in pat.finditer(analysis_text):
            phrase = m.group()
            line_no = get_line_for_position(body_lines, body_line_map, m.start())
            findings.append({
                "line": line_no,
                "phrase": phrase,
            })
    return {
        "count": len(findings),
        "items": findings,
        "flag": len(findings) > THRESH_PADDING_MAX,
    }


def analyze_product_descriptions(analysis_text: str, raw_lines, body_lines, body_line_map):
    """
    Detect product-description appositives:
    TOOL_NAME, a/an ADJECTIVE NOUN that/which ...
    e.g. "Autograder4Canvas, an equity-centered teacher automation tool that surfaces..."
    """
    # Match: capitalized word(s) or known tool names, comma, a/an, then adjective(s)+noun, then that/which
    pat = re.compile(
        r"([A-Z][A-Za-z0-9_]*(?:\s+[A-Z][A-Za-z0-9_]*)*)"  # Tool name (capitalized)
        r",\s+an?\s+"                                         # , a/an
        r"((?:\w+[\s-])*\w+)"                                # adjective(s) + noun phrase
        r"\s+(?:that|which)\b",                               # that/which
        re.MULTILINE,
    )
    findings = []
    for m in pat.finditer(analysis_text):
        tool_name = m.group(1)
        descriptor = m.group(2)
        full_match = m.group(0)
        line_no = get_line_for_position(body_lines, body_line_map, m.start())
        findings.append({
            "line": line_no,
            "tool": tool_name,
            "descriptor": descriptor,
            "text": full_match[:100],
        })
    return {
        "count": len(findings),
        "items": findings,
        "flag": len(findings) > THRESH_PRODUCT_MAX,
    }


def analyze_corporate_jargon(analysis_text: str, raw_lines, body_lines, body_line_map):
    findings = []
    for pattern_str in CORPORATE_JARGON:
        pat = re.compile(pattern_str, re.IGNORECASE)
        for m in pat.finditer(analysis_text):
            phrase = m.group()
            line_no = get_line_for_position(body_lines, body_line_map, m.start())
            ctx = context_snippet(analysis_text, m.start(), m.end())
            findings.append({
                "line": line_no,
                "phrase": phrase,
                "context": ctx,
            })
    return {
        "count": len(findings),
        "items": findings,
        "flag": len(findings) > THRESH_JARGON_MAX,
    }


def analyze_front_loading(text: str, raw_lines, body_lines, body_line_map) -> dict:
    """Flag sentences with heavy subjects (many content words before the main verb).

    Content word POS tags counted: NN*, JJ*, RB*, VBG
    Main verb POS tags (predicate onset): VBP, VBZ, VBD, VB, MD
    Sentences under 6 words are skipped.
    Existential 'There is/are...' constructions are skipped.
    Threshold: >8 content words before main verb.
    Flag triggered: >2 heavy-subject sentences in the document.
    """
    sentences = sent_tokenize(text)
    heavy = []

    for sent in sentences:
        words = word_tokenize(sent)
        if len(words) < 6:
            continue
        tagged = pos_tag(words)

        # Find first main verb; count content words before it
        content_before_verb = 0
        found_verb = False
        for i, (word, tag) in enumerate(tagged):
            if tag in ('VBP', 'VBZ', 'VBD', 'VB', 'MD'):
                # Skip existential "There is/are" constructions
                if i == 1 and tagged[0][0].lower() == 'there':
                    break
                found_verb = True
                break
            if tag.startswith(('NN', 'JJ', 'RB', 'VBG')):
                content_before_verb += 1

        if not found_verb:
            continue

        if content_before_verb > 8:
            # Find line number by matching sentence text against body lines
            line_no = get_line_for_position(
                body_lines, body_line_map,
                text.find(sent[:40]) if sent[:40] in text else 0
            )
            heavy.append({
                "text": sent[:120],
                "subject_weight": content_before_verb,
                "line": line_no,
            })

    return {
        "heavy_subject_count": len(heavy),
        "heavy_subject_max": max((h["subject_weight"] for h in heavy), default=0),
        "examples": heavy[:5],
        "flag": len(heavy) > 2,
    }


# ---------------------------------------------------------------------------
# Paragraph and cohesion analysis (added 2026-05)
# ---------------------------------------------------------------------------

def analyze_paragraphs(text: str) -> dict:
    """Paragraph-level structural metrics.

    Splits text into paragraphs by double newlines, skipping anything under 5 words
    (likely headers or empty lines). For each paragraph, records sentence count,
    first-sentence length (proxy for topic sentence weight), and last-sentence
    length (proxy for landing weight).
    """
    paras = [p.strip() for p in re.split(r'\n{2,}', text.strip()) if p.strip()]
    paragraphs = []
    for p in paras:
        words = p.split()
        if len(words) < 5:
            continue
        sents = sent_tokenize(p)
        if not sents:
            continue
        first_sent_words = len(sents[0].split())
        last_sent_words = len(sents[-1].split())
        paragraphs.append({
            "sentence_count": len(sents),
            "first_sentence_words": first_sent_words,
            "last_sentence_words": last_sent_words,
        })

    if not paragraphs:
        return {
            "paragraph_count": 0,
            "avg_sentences_per_paragraph": 0.0,
            "paragraph_length_stdev": 0.0,
            "short_paragraph_count": 0,
            "long_paragraph_count": 0,
            "first_sentence_lengths": [],
            "last_sentence_lengths": [],
            "avg_first_sentence_words": 0.0,
            "avg_last_sentence_words": 0.0,
        }

    sentence_counts = [p["sentence_count"] for p in paragraphs]
    first_lens = [p["first_sentence_words"] for p in paragraphs]
    last_lens = [p["last_sentence_words"] for p in paragraphs]
    mean_sc = sum(sentence_counts) / len(sentence_counts)
    var_sc = sum((x - mean_sc) ** 2 for x in sentence_counts) / len(sentence_counts)
    stdev_sc = var_sc ** 0.5

    return {
        "paragraph_count": len(paragraphs),
        "avg_sentences_per_paragraph": round(mean_sc, 2),
        "paragraph_length_stdev": round(stdev_sc, 2),
        "short_paragraph_count": sum(1 for c in sentence_counts if c == 1),
        "long_paragraph_count": sum(1 for c in sentence_counts if c >= 5),
        "first_sentence_lengths": first_lens,
        "last_sentence_lengths": last_lens,
        "avg_first_sentence_words": round(sum(first_lens) / len(first_lens), 1),
        "avg_last_sentence_words": round(sum(last_lens) / len(last_lens), 1),
    }


# Common stop words for cohesion analysis (excluded from content word overlap)
_COHESION_STOPWORDS = set("""
the a an and or but if then else when where what who whom whose which that this these those
i me my mine you your yours he him his she her hers it its we us our ours they them their theirs
is am are was were be been being have has had do does did will would shall should can could may
might must of in on at to for with by from as into about against between through during before
after above below up down out off over under again further once here there only own same so than
too very just not no nor any all each every both few more most other some such own
""".split())


def _content_words(sentence: str) -> set:
    """Extract content words from a sentence for cohesion comparison.

    Tries POS tagging if nltk is available; falls back to heuristic
    (lowercased words >3 chars, excluding stop words).
    """
    words = re.findall(r"[A-Za-z']+", sentence.lower())
    try:
        tagged = pos_tag(words)
        content = {
            w for w, t in tagged
            if (t.startswith('NN') or t.startswith('JJ') or
                (t.startswith('VB') and t not in ('VBP', 'VBZ')))
            and w not in _COHESION_STOPWORDS and len(w) > 3
        }
        if content:
            return content
    except Exception:
        pass
    return {w for w in words if w not in _COHESION_STOPWORDS and len(w) > 3}


def analyze_cohesion(text: str) -> dict:
    """Sentence-to-sentence cohesion proxy via lexical chain density.

    For each adjacent sentence pair, compute content word overlap ratio.
    Low overlap (< 0.1) flags potential cohesion breaks where adjacent
    sentences share no referential grounding.
    """
    sentences = sent_tokenize(text)
    if len(sentences) < 2:
        return {
            "mean_adjacency_overlap": 0.0,
            "low_cohesion_pair_count": 0,
            "low_cohesion_pairs": [],
            "cohesion_score": 0.0,
            "total_pairs": 0,
        }

    overlaps = []
    low_pairs = []
    for i in range(len(sentences) - 1):
        s1, s2 = sentences[i], sentences[i + 1]
        c1, c2 = _content_words(s1), _content_words(s2)
        if not c1 or not c2:
            continue
        shared = c1 & c2
        avg_size = (len(c1) + len(c2)) / 2
        overlap = len(shared) / avg_size if avg_size > 0 else 0.0
        overlaps.append(overlap)
        if overlap < 0.1:
            low_pairs.append({
                "sent1_preview": s1[:80] + ('...' if len(s1) > 80 else ''),
                "sent2_preview": s2[:80] + ('...' if len(s2) > 80 else ''),
                "overlap": round(overlap, 3),
            })

    if not overlaps:
        return {
            "mean_adjacency_overlap": 0.0,
            "low_cohesion_pair_count": 0,
            "low_cohesion_pairs": [],
            "cohesion_score": 0.0,
            "total_pairs": 0,
        }

    mean_overlap = sum(overlaps) / len(overlaps)
    # Cohesion score: 0–10 scale (0.4+ overlap = 10, 0 overlap = 0)
    score = min(10.0, max(0.0, mean_overlap * 25))

    return {
        "mean_adjacency_overlap": round(mean_overlap, 3),
        "low_cohesion_pair_count": len(low_pairs),
        "low_cohesion_pairs": low_pairs[:5],
        "cohesion_score": round(score, 1),
        "total_pairs": len(overlaps),
    }


# ---------------------------------------------------------------------------
# Flagged sentences collector
# ---------------------------------------------------------------------------

def collect_flagged_sentences(analysis_text, raw_lines, body_lines, body_line_map, results):
    """Collect all individually flagged sentences with reasons."""
    flagged = []

    # Long sentences
    for sent, wc in results["sentences"]["over_long"]:
        line_no = find_line_number(raw_lines, sent)
        reason = f"Sentence is {wc} words (>{THRESH_LONG_SENT})"
        if wc > THRESH_REWRITE_SENT:
            reason += " — REWRITE"
        flagged.append({"line": line_no, "sentence": sent.strip()[:120], "reason": reason})

    # Hedge words
    for item in results["hedges"]["items"]:
        flagged.append({
            "line": item["line"],
            "sentence": item["context"],
            "reason": f"Hedge word: \"{item['word']}\"",
        })

    # Self-aggrandizing
    for item in results["aggrandizing"]["items"]:
        flagged.append({
            "line": item["line"],
            "sentence": item["context"],
            "reason": f"Self-aggrandizing frame: \"{item['phrase']}\"",
        })

    # Topic sentences
    for item in results["topic_sentences"]["items"]:
        flagged.append({
            "line": item["line"],
            "sentence": item["text"],
            "reason": "\"This is\"/\"These are\"/\"That is\" topic sentence opener",
        })

    # Long em-dash insertions
    for item in results["emdashes"]["long_insertions"]:
        flagged.append({
            "line": item["line"],
            "sentence": item["text"],
            "reason": f"Em-dash insertion is {item['word_count']} words (>{THRESH_EMDASH_INSERT_WORDS})",
        })

    # Narrative padding
    for item in results["padding"]["items"]:
        flagged.append({
            "line": item["line"],
            "sentence": item["phrase"],
            "reason": "Narrative padding phrase",
        })

    # Product descriptions
    for item in results["product_descriptions"]["items"]:
        flagged.append({
            "line": item["line"],
            "sentence": item["text"],
            "reason": f"Product-description appositive for \"{item['tool']}\"",
        })

    # Corporate jargon
    for item in results.get("corporate_jargon", {}).get("items", []):
        flagged.append({
            "line": item["line"],
            "sentence": item["context"],
            "reason": f"Corporate jargon: \"{item['phrase']}\"",
        })

    # Sort by line number
    flagged.sort(key=lambda x: x["line"])
    return flagged


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def flag_marker(flagged: bool) -> str:
    return " [FLAG]" if flagged else ""


def format_report(filepath: str, results: dict, flagged_sentences: list) -> str:
    filename = os.path.basename(filepath)
    wc = results["words"]
    ss = results["sentences"]
    ed = results["emdashes"]
    hd = results["hedges"]
    ag = results["aggrandizing"]
    ts = results["topic_sentences"]
    cn = results["connectors"]
    pv = results["passive"]
    rd = results["readability"]
    pd = results["padding"]
    pr = results["product_descriptions"]
    cj = results.get("corporate_jargon", {"count": 0, "items": [], "flag": False})
    fl = results.get("front_loading", {"heavy_subject_count": 0, "heavy_subject_max": 0,
                                       "examples": [], "flag": False})

    sign = "+" if wc["pct_diff"] >= 0 else ""

    lines = []
    lines.append("")
    lines.append("\u2550" * 51)
    lines.append("  VOICING REPORT: " + filename)
    lines.append("\u2550" * 51)
    lines.append("")

    # Word count
    lines.append("WORD COUNT")
    lines.append(f"  Total: {wc['total']} words ({sign}{wc['pct_diff']}% vs target {wc['target']})"
                 + flag_marker(wc["flag"]))
    lines.append("")

    # Sentence structure
    lines.append("SENTENCE STRUCTURE")
    lines.append(f"  Sentences: {ss['count']} | Avg: {ss['avg_length']} words | Max: {ss['max_length']} words")
    lines.append(f"  Over {ss['long_threshold']} words: {ss['over_long_count']} sentences"
                 + flag_marker(ss["flag_long"]))
    lines.append(f"  Over {ss['rewrite_threshold']} words: {ss['over_rewrite_count']} sentences"
                 + flag_marker(ss["flag_rewrite"]))
    lines.append("")

    # Em-dash usage
    lines.append("EM-DASH USAGE")
    lines.append(f"  Total: {ed['total']} ({ed['per_1000']}/1000 words)"
                 + flag_marker(ed["flag_density"]))
    lines.append(f"  Insertions >{THRESH_EMDASH_INSERT_WORDS} words: {len(ed['long_insertions'])}"
                 + flag_marker(ed["flag_insertions"]))
    for ins in ed["long_insertions"]:
        lines.append(f"    Line {ins['line']}: \"{ins['text']}\" ({ins['word_count']} words)")
    lines.append("")

    # Modality / Stance
    lines.append("MODALITY / STANCE")
    lines.append(f"  Hedge words: {hd['count']}" + flag_marker(hd["flag"]))
    for item in hd["items"]:
        lines.append(f"    Line {item['line']}: \"{item['word']}\" \u2014 \"{item['context']}\"")
    lines.append(f"  Self-aggrandizing frames: {ag['count']}" + flag_marker(ag["flag"]))
    for item in ag["items"]:
        lines.append(f"    Line {item['line']}: \"{item['phrase']}\" \u2014 \"{item['context']}\"")
    lines.append("")

    # Topic sentences
    lines.append("TOPIC SENTENCES")
    lines.append(f"  \"This is/These are/That is\" openers: {ts['count']}"
                 + flag_marker(ts["flag"]))
    for item in ts["items"]:
        lines.append(f"    Line {item['line']}: \"{item['text']}\"")
    lines.append("")

    # Cohesion
    lines.append("COHESION")
    lines.append(f"  Logical connectors: {cn['count']}" + flag_marker(cn["flag"]))
    for item in cn["items"]:
        lines.append(f"    Line {item['line']}: \"{item['word']}\"")
    lines.append(f"  Passive voice (approx): {pv['count']}")
    lines.append("")

    # Readability
    lines.append("READABILITY")
    lines.append(f"  Flesch-Kincaid: {rd['flesch_kincaid']} | Gunning Fog: {rd['gunning_fog']} | Flesch Reading: {rd['flesch_reading_ease']}")
    lines.append("")

    # Narrative patterns
    lines.append("NARRATIVE PATTERNS")
    lines.append(f"  Padding phrases: {pd['count']}" + flag_marker(pd["flag"]))
    for item in pd["items"]:
        lines.append(f"    Line {item['line']}: \"{item['phrase']}\"")
    lines.append(f"  Product descriptions: {pr['count']}" + flag_marker(pr["flag"]))
    for item in pr["items"]:
        lines.append(f"    Line {item['line']}: \"{item['text']}\"")
    lines.append(f"  Corporate jargon: {cj['count']}" + flag_marker(cj["flag"]))
    for item in cj["items"]:
        lines.append(f"    Line {item['line']}: \"{item['phrase']}\" \u2014 \"{item['context']}\"")
    lines.append("")

    # Front-loading
    lines.append("FRONT-LOADING")
    lines.append(f"  Heavy subjects (>8 content words before main verb): {fl['heavy_subject_count']}"
                 + flag_marker(fl["flag"]))
    if fl["heavy_subject_max"] > 0:
        lines.append(f"  Max subject weight: {fl['heavy_subject_max']} content words")
    for ex in fl["examples"]:
        line_info = f"Line {ex['line']}: " if ex.get("line") else ""
        lines.append(f"    {line_info}\"{ex['text']}\" ({ex['subject_weight']} content words)")
    lines.append("")

    # Flagged sentences
    lines.append("\u2550" * 51)
    lines.append("  FLAGGED SENTENCES (review these)")
    lines.append("\u2550" * 51)
    lines.append("")

    if flagged_sentences:
        for fs in flagged_sentences:
            lines.append(f"  Line {fs['line']}: {fs['reason']}")
            lines.append(f"    \"{fs['sentence']}\"")
            lines.append("")
    else:
        lines.append("  No flagged sentences.")
        lines.append("")

    # Summary
    lines.append("\u2550" * 51)
    lines.append("  SUMMARY")
    lines.append("\u2550" * 51)
    lines.append("")

    # Count total flags, distinguishing voice flags (diagnostic of agent writing)
    # from structural flags (may reflect deliberate style choices)
    flag_breakdown = {}
    voice_flags = 0  # hedges, aggrandizing, padding, product descs — diagnostic
    structural_flags = 0  # long sentences, em-dashes — may be deliberate

    if wc["flag"]:
        flag_breakdown["word count"] = 1
        structural_flags += 1
    if ss["flag_long"]:
        flag_breakdown[f"long sentences (>{ss['long_threshold']}w)"] = ss["over_long_count"]
        structural_flags += ss["over_long_count"]
    if ss["flag_rewrite"]:
        flag_breakdown[f"rewrite sentences (>{ss['rewrite_threshold']}w)"] = ss["over_rewrite_count"]
        structural_flags += ss["over_rewrite_count"]
    if ed["flag_density"]:
        flag_breakdown["em-dash density"] = 1
        structural_flags += 1
    if ed["flag_insertions"]:
        flag_breakdown["em-dash insertions"] = len(ed["long_insertions"])
        structural_flags += len(ed["long_insertions"])
    if hd["flag"]:
        flag_breakdown["hedge words"] = hd["count"]
        voice_flags += hd["count"]
    if ag["flag"]:
        flag_breakdown["self-aggrandizing"] = ag["count"]
        voice_flags += ag["count"]
    if ts["flag"]:
        flag_breakdown["topic sentence openers"] = ts["count"]
        voice_flags += ts["count"]
    if cn["flag"]:
        flag_breakdown["logical connectors"] = cn["count"]
        voice_flags += cn["count"]
    if pd["flag"]:
        flag_breakdown["padding phrases"] = pd["count"]
        voice_flags += pd["count"]
    if pr["flag"]:
        flag_breakdown["product descriptions"] = pr["count"]
        voice_flags += pr["count"]
    if cj["flag"]:
        flag_breakdown["corporate jargon"] = cj["count"]
        voice_flags += cj["count"]
    if fl["flag"]:
        flag_breakdown["front-loaded subjects"] = fl["heavy_subject_count"]
        voice_flags += fl["heavy_subject_count"]

    total_flags = sum(flag_breakdown.values())
    breakdown_str = ", ".join(f"{v} {k}" for k, v in flag_breakdown.items())

    lines.append(f"  Flags: {total_flags} total ({voice_flags} voice, {structural_flags} structural)" +
                 (f" — {breakdown_str}" if breakdown_str else " (clean)"))

    # Overall assessment: voice flags are more diagnostic than structural flags
    # A document can have several long sentences and em-dash insertions as
    # deliberate style, but hedge words and self-aggrandizing frames are always
    # agent artifacts.
    if total_flags == 0:
        lines.append("  Draft passes quantitative voicing checks. Proceed to qualitative CDA review.")
    elif voice_flags == 0 and structural_flags <= 15:
        lines.append("  Draft has structural flags only (no voice flags). Review long sentences and em-dashes, then proceed to qualitative CDA review.")
    elif voice_flags <= 2 and total_flags <= 8:
        lines.append("  Draft has minor quantitative issues. Review flagged items, then proceed to qualitative CDA review.")
    elif voice_flags <= 4 and total_flags <= 15:
        lines.append("  Draft has notable quantitative issues. Address voice flags before qualitative review.")
    else:
        lines.append("  Draft has significant quantitative issues typical of agent-generated text. Recommend revision pass before qualitative review.")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Citation tracking and DIAGNOSTIC REVIEW auto-trigger
# ---------------------------------------------------------------------------

def _scan_text_for_check_ids(text: str, profile: dict) -> list:
    """Return sorted list of qualitative check IDs that appear in `text`
    with word-boundary match. Uses re.escape on each ID for safety."""
    ids = [c.get("id", "") for c in profile.get("qualitative", []) if c.get("id")]
    found = set()
    for cid in ids:
        if not cid:
            continue
        if re.search(r"\b" + re.escape(cid) + r"\b", text):
            found.add(cid)
    return sorted(found)


def _load_citation_log() -> dict:
    """Load citation_log.json, creating an empty structure if absent or unreadable."""
    if not os.path.exists(CITATION_LOG_PATH):
        return {"runs": []}
    try:
        with open(CITATION_LOG_PATH, "r") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "runs" not in data:
            return {"runs": []}
        return data
    except Exception:
        return {"runs": []}


def _append_citation_log(command: str, files: list, cited_check_ids: list):
    """Append a new run entry to citation_log.json."""
    log = _load_citation_log()
    log.setdefault("runs", []).append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "command": command,
        "files": list(files),
        "cited_check_ids": list(cited_check_ids),
    })
    try:
        with open(CITATION_LOG_PATH, "w") as f:
            json.dump(log, f, indent=2)
    except Exception as e:
        print(f"  (citation log write failed: {e})", file=sys.stderr)


def _silent_diagnostics(profile: dict, log: dict, threshold: int = DIAGNOSTIC_SILENCE_THRESHOLD):
    """Return list of (id, last_cited_iso_or_None) for diagnostic-role checks
    that have NOT been cited in the last `threshold` runs.

    Returns [] if there are fewer than `threshold` runs total (need history first).
    """
    runs = log.get("runs", [])
    if len(runs) < threshold:
        return []
    diagnostic_ids = [c["id"] for c in profile.get("qualitative", []) if c.get("role") == "diagnostic"]
    if not diagnostic_ids:
        return []
    recent = runs[-threshold:]
    silent = []
    for cid in diagnostic_ids:
        cited_recently = any(cid in r.get("cited_check_ids", []) for r in recent)
        if cited_recently:
            continue
        # find last citation (anywhere in log) for reporting
        last = None
        for r in reversed(runs):
            if cid in r.get("cited_check_ids", []):
                last = r.get("timestamp")
                break
        silent.append((cid, last))
    return silent


def emit_cited_checks_and_update_log(scanned_text: str, profile: dict,
                                     command: str, files: list):
    """Called at end of --learn / --learn-sequence reports.

    1. Scans accumulated analysis text for check ID citations.
    2. Prints CITED CHECKS THIS REVISION banner.
    3. Appends entry to citation_log.json.
    4. If any diagnostic check has been silent for DIAGNOSTIC_SILENCE_THRESHOLD
       runs, prints DIAGNOSTIC REVIEW DUE block.
    """
    sep = "═" * 51
    cited = _scan_text_for_check_ids(scanned_text, profile)

    print(f"\n{sep}")
    print("  CITED CHECKS THIS REVISION")
    print(sep)
    if cited:
        # break into lines of ~72 chars for readability
        line = "    "
        out_lines = []
        for cid in cited:
            chunk = cid + ", "
            if len(line) + len(chunk) > 76 and line.strip():
                out_lines.append(line.rstrip(", "))
                line = "    " + chunk
            else:
                line += chunk
        if line.strip():
            out_lines.append(line.rstrip(", "))
        print("\n".join(out_lines))
    else:
        print("    (none)")

    # Persist
    _append_citation_log(command, files, cited)

    # DIAGNOSTIC REVIEW auto-trigger
    log = _load_citation_log()
    silent = _silent_diagnostics(profile, log)
    if silent:
        print(f"\n{sep}")
        print("  DIAGNOSTIC REVIEW DUE")
        print(sep)
        print(f"  The following diagnostic checks have not been cited in the "
              f"last {DIAGNOSTIC_SILENCE_THRESHOLD} learn runs:")
        for cid, last in silent:
            last_str = f"last cited: {last[:10]}" if last else "never cited"
            print(f"    - {cid} ({last_str})")
        print("  Run `python3 writing_check.py --audit-diagnostics` to review "
              "and decide whether to keep, demote (cut), or rephrase to fire "
              "more reliably.")


def log_cited_checks_postanalysis(cited_ids: list, profile_path: str = None):
    """Append cited check IDs to the most recent run entry in citation_log.json.

    Called by agents after their Phase 4 CDA sweep, to record which check
    IDs fired during the revision they just analyzed. Closes the gap left
    by --learn's text-scan, which only sees what the script printed (not
    the agent's post-script analysis).
    """
    if not os.path.exists(CITATION_LOG_PATH):
        print(f"Error: No citation log at {CITATION_LOG_PATH}. "
              f"Run --learn or --learn-sequence first.", file=sys.stderr)
        sys.exit(1)
    log = _load_citation_log()
    runs = log.get("runs", [])
    if not runs:
        print(f"Error: Citation log is empty. Run --learn first.", file=sys.stderr)
        sys.exit(1)

    # Validate IDs against the loaded profile
    if profile_path or True:
        try:
            if not profile_path:
                profile_path = discover_profile()
            profile = load_profile(profile_path)
            valid_ids = {c["id"] for c in profile.get("qualitative", []) if c.get("id")}
            unknown = [cid for cid in cited_ids if cid not in valid_ids]
            if unknown:
                print(f"  Warning: unknown check IDs (not in profile): {unknown}",
                      file=sys.stderr)
        except Exception:
            pass  # Validation is best-effort

    # Merge into most recent run's cited_check_ids (dedup, sort)
    last = runs[-1]
    existing = set(last.get("cited_check_ids", []))
    new_total = sorted(existing | set(cited_ids))
    last["cited_check_ids"] = new_total

    with open(CITATION_LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

    sep = "═" * 51
    print(f"\n{sep}")
    print("  CITED CHECKS LOGGED (post-analysis)")
    print(sep)
    print(f"  Run timestamp: {last.get('timestamp', '?')}")
    print(f"  Run command:   {last.get('command', '?')}")
    print(f"  Files:         {last.get('files', [])}")
    print(f"  Cited (total): {len(new_total)} check IDs")
    if new_total:
        print(f"    {', '.join(new_total)}")


def run_audit_diagnostics(profile_path: str = None):
    """Read-only report on diagnostic-role checks: last cited dates and
    counts over recent history. Doesn't modify anything; surfaces data for
    the user to act on."""
    sep = "═" * 51

    # Load profile (auto-discover if not specified)
    if not profile_path:
        try:
            profile_path = discover_profile()
        except SystemExit:
            raise
    profile = load_profile(profile_path)
    profile_name = os.path.basename(profile_path)
    profile_version = profile.get("profile", {}).get("version", "?")

    # Load citation log
    if not os.path.exists(CITATION_LOG_PATH):
        print(f"\n{sep}")
        print("  DIAGNOSTIC CHECK STATUS REPORT")
        print(sep)
        print(f"\n  No citation log yet at {CITATION_LOG_PATH}.")
        print("  Run --learn or --learn-sequence first to generate citation history.")
        return
    log = _load_citation_log()
    runs = log.get("runs", [])

    diagnostic_checks = [c for c in profile.get("qualitative", []) if c.get("role") == "diagnostic"]

    print(f"\n{sep}")
    print("  DIAGNOSTIC CHECK STATUS REPORT")
    print(sep)
    print(f"  Profile: {profile_name} (v{profile_version})")
    print(f"  Total runs in citation log: {len(runs)}")
    print(f"  Diagnostic checks: {len(diagnostic_checks)}")
    print()
    print("  CHECK STATUS")

    # Recent window for counts
    recent_window = 10
    recent = runs[-recent_window:] if runs else []

    silent_in_threshold = []
    for c in diagnostic_checks:
        cid = c["id"]
        # Last citation timestamp (any time)
        last_iso = None
        for r in reversed(runs):
            if cid in r.get("cited_check_ids", []):
                last_iso = r.get("timestamp")
                break
        # Count over last 10 runs
        count_recent = sum(1 for r in recent if cid in r.get("cited_check_ids", []))
        # Status
        if last_iso is None:
            status = "SILENT (never cited)"
            silent_in_threshold.append(cid)
        elif count_recent == 0:
            # cited at some point but not in the last 10 runs
            status = "SILENT (consider review)"
            silent_in_threshold.append(cid)
        else:
            status = "FIRING (recent)"

        print()
        print(f"  {cid}")
        if last_iso:
            # Compute "N runs ago" — find index from end
            runs_ago = None
            for i, r in enumerate(reversed(runs)):
                if cid in r.get("cited_check_ids", []):
                    runs_ago = i
                    break
            ago_str = f" ({runs_ago} run{'s' if runs_ago != 1 else ''} ago)" if runs_ago is not None else ""
            print(f"    Last cited: {last_iso[:10]}{ago_str}")
        else:
            print(f"    Last cited: never")
        print(f"    Citations in last {recent_window} runs: {count_recent}")
        print(f"    Status: {status}")

    print()
    print("  RECOMMENDATIONS")
    print("    SILENT diagnostic checks may be:")
    print("    - working as insurance (fire only when triggered, by design)")
    print("    - poorly worded (failing to fire when they should)")
    print("    - dead (no longer relevant)")
    print("    Decide for each: keep, rephrase, or cut.")


# ---------------------------------------------------------------------------
# Learning loop: update profile from revision pair
# ---------------------------------------------------------------------------

def learn_from_revision(first_draft_path: str, final_draft_path: str, profile_path: str,
                        notes: str = "", update_profile: bool = True,
                        genre: str = None):
    """
    Compare an agent first draft to a human-revised final draft.

    Pipeline:
      1. Diff analysis \u2014 sentence-level change classification, paragraph reorder detection
      2. Quantitative update \u2014 stylometry, perplexity, embeddings via EMA
      3. Paragraph + cohesion metrics \u2014 structural and sentence-to-sentence flow comparison
      4. Qualitative analysis prompt \u2014 guidance for the agent's CDA sweep

    If update_profile is False (--quantitative mode), no profile changes are written.

    Genre/voice separation:
        When `genre` is specified and profile["genres"][genre]["stylometry"]
        exists, the revision shift is decomposed into genre-direction and
        voice-direction components. The genre centroid absorbs the genre
        component; the user centroid absorbs only the voice residual.

        When `genre` is specified but no genre centroid exists yet, the genre
        centroid is bootstrapped from the final draft's stylometry (seeded
        with revision_count = 1) and the user centroid update follows the
        original (full-shift) behavior \u2014 same as if genre were not specified.

        When `genre` is None, behavior is unchanged: user centroid absorbs
        the full revision shift via EMA.
    """
    try:
        from stylometry import compute_stylometry, compare_stylometry, update_profile_stylometry
    except ImportError:
        print("Error: stylometry.py not found. Cannot run --learn mode.", file=sys.stderr)
        sys.exit(1)

    profile = load_profile(profile_path)

    if "stylometry" not in profile:
        print(
            "Error: Profile has no stylometry section. "
            "Run --calibrate first to build the voice fingerprint.",
            file=sys.stderr
        )
        sys.exit(1)

    with open(first_draft_path, "r", encoding="utf-8") as f:
        first_text = f.read()
    with open(final_draft_path, "r", encoding="utf-8") as f:
        final_text = f.read()

    sep = "\u2550" * 51

    # Print report header
    print(f"\n{sep}")
    print("  REVISION LEARNING REPORT")
    print(sep)
    print(f"\n  First draft:  {os.path.basename(first_draft_path)}")
    print(f"  Final draft:  {os.path.basename(final_draft_path)}")
    print(f"  Profile:      {os.path.basename(profile_path)}")
    if notes:
        print(f"  Notes:        {notes}")
    if not update_profile:
        print(f"  Mode:         QUANTITATIVE ONLY (no profile update)")

    # --- Phase 1: Diff analysis ---
    diff_result = None
    diff_report_str = ""
    try:
        from diff_analysis import compute_diff, format_diff_report
        diff_result = compute_diff(first_text, final_text)
        diff_report_str = format_diff_report(diff_result)
        print(diff_report_str)
    except ImportError:
        print("\n  (diff_analysis module not available \u2014 skipping structural diff)")

    # --- Phase 2: Stylometry ---
    first_stylo = compute_stylometry(first_text)
    final_stylo = compute_stylometry(final_text)

    # Decide whether genre/voice decomposition applies. Three cases:
    #   (a) no genre flag                 → original behavior
    #   (b) genre flag, genre centroid exists → decompose, update both
    #   (c) genre flag, no genre centroid → bootstrap genre, update user fully
    genre_centroid = None
    bootstrap_genre = False
    if genre:
        genre_block = profile.get("genres", {}).get(genre, {}) or {}
        genre_centroid = genre_block.get("stylometry")
        if genre_centroid is None:
            bootstrap_genre = True

    if genre and not bootstrap_genre and genre_centroid is not None:
        # ----- Case (b): decompose -----
        try:
            from genre_separation import (
                decompose_stylometric_shift,
                update_genre_centroid_via_ema,
                update_user_centroid_via_ema_voice_only,
                format_decomposition_report,
            )
        except ImportError:
            print("Warning: genre_separation.py not found — falling back to "
                  "non-decomposed update.", file=sys.stderr)
            stylo_comparison = compare_stylometry(first_stylo, final_stylo, profile["stylometry"])
            print(f"\n  STYLOMETRY")
            print(f"  {stylo_comparison['summary']}")
            updated = update_profile_stylometry(profile, first_stylo, final_stylo)
        else:
            from stylometry import _ema_alpha, generate_style_notes
            user_centroid = profile["stylometry"]
            decomp = decompose_stylometric_shift(
                user_centroid, genre_centroid, first_stylo, final_stylo
            )
            print()
            print(format_decomposition_report(decomp, genre))

            # Apply EMAs
            user_rev_count = user_centroid.get("revision_count", 0)
            genre_rev_count = genre_centroid.get("revision_count", 0)
            user_alpha = _ema_alpha(user_rev_count)
            genre_alpha = _ema_alpha(genre_rev_count)

            new_user_centroid = update_user_centroid_via_ema_voice_only(
                user_centroid, decomp["voice_components"], user_alpha
            )
            new_user_centroid["revision_count"] = user_rev_count + 1
            # Refresh style_notes occasionally (mirrors stylometry module schedule)
            new_count = new_user_centroid["revision_count"]
            if new_count == 1 or new_count % 3 == 0:
                new_user_centroid["style_notes"] = generate_style_notes(new_user_centroid)

            new_genre_centroid = update_genre_centroid_via_ema(
                genre_centroid, decomp["genre_components"], genre_alpha
            )
            new_genre_centroid["revision_count"] = genre_rev_count + 1
            new_g_count = new_genre_centroid["revision_count"]
            if new_g_count == 1 or new_g_count % 3 == 0:
                new_genre_centroid["style_notes"] = generate_style_notes(new_genre_centroid)

            import copy as _copy
            updated = _copy.deepcopy(profile)
            updated["stylometry"] = new_user_centroid
            updated.setdefault("genres", {})
            if genre not in updated["genres"] or not isinstance(updated["genres"][genre], dict):
                updated["genres"][genre] = {}
            updated["genres"][genre]["stylometry"] = new_genre_centroid

            print(
                f"\n  Profile updated: genre '{genre}' centroid "
                f"(rev count: {new_genre_centroid['revision_count']}), "
                f"user centroid (rev count: {new_user_centroid['revision_count']})"
            )
            # Mark the path we took so the writer at the end of the function
            # knows to persist the genre block (not just root stylometry).
            updated["_genre_separation_applied"] = genre

    elif genre and bootstrap_genre:
        # ----- Case (c): bootstrap genre centroid from this revision pair -----
        try:
            from genre_separation import seed_genre_centroid_from_stylometry
        except ImportError:
            print("Warning: genre_separation.py not found — bootstrapping is "
                  "unavailable. Falling back to non-decomposed update.",
                  file=sys.stderr)
            stylo_comparison = compare_stylometry(first_stylo, final_stylo, profile["stylometry"])
            print(f"\n  STYLOMETRY")
            print(f"  {stylo_comparison['summary']}")
            updated = update_profile_stylometry(profile, first_stylo, final_stylo)
        else:
            print(f"\n  STYLOMETRY (bootstrapping genre centroid '{genre}' from this revision pair)")
            stylo_comparison = compare_stylometry(first_stylo, final_stylo, profile["stylometry"])
            print(f"  {stylo_comparison['summary']}")
            seeded = seed_genre_centroid_from_stylometry(final_stylo)
            updated = update_profile_stylometry(profile, first_stylo, final_stylo)
            updated.setdefault("genres", {})
            if genre not in updated["genres"] or not isinstance(updated["genres"][genre], dict):
                updated["genres"][genre] = {
                    "description": f"Auto-created by --learn --genre {genre}",
                }
            updated["genres"][genre]["stylometry"] = seeded
            updated["_genre_separation_applied"] = genre
            print(f"\n  Bootstrapped: profile.genres.{genre}.stylometry "
                  f"(revision_count = 1). Subsequent --learn --genre {genre} runs "
                  f"will decompose against this centroid.")
    else:
        # ----- Case (a): original behavior -----
        stylo_comparison = compare_stylometry(first_stylo, final_stylo, profile["stylometry"])
        print(f"\n  STYLOMETRY")
        print(f"  {stylo_comparison['summary']}")
        updated = update_profile_stylometry(profile, first_stylo, final_stylo)

    # --- Perplexity (optional) ---
    if "perplexity" in updated:
        try:
            from perplexity import compute_perplexity, compare_perplexity, update_profile_perplexity
            first_ppl = compute_perplexity(first_text)
            final_ppl = compute_perplexity(final_text)
            if first_ppl and final_ppl:
                ppl_comparison = compare_perplexity(first_ppl, final_ppl, updated["perplexity"])
                print(f"\n  PERPLEXITY")
                print(f"  {ppl_comparison['summary']}")
                updated = update_profile_perplexity(updated, first_ppl, final_ppl)
        except ImportError:
            pass

    # --- Embeddings (optional) ---
    if "embeddings" in updated:
        try:
            from embeddings import compute_embeddings, compare_embeddings, update_profile_embeddings
            first_emb = compute_embeddings(first_text)
            final_emb = compute_embeddings(final_text)
            if first_emb and final_emb:
                emb_comparison = compare_embeddings(first_emb, final_emb, updated["embeddings"])
                print(f"\n  EMBEDDINGS")
                print(f"  {emb_comparison['summary']}")
                updated = update_profile_embeddings(updated, first_emb, final_emb)
        except ImportError:
            pass

    # --- Phase 3: Paragraph + cohesion comparison ---
    first_para = analyze_paragraphs(first_text)
    final_para = analyze_paragraphs(final_text)
    first_coh = analyze_cohesion(first_text)
    final_coh = analyze_cohesion(final_text)

    print(f"\n  PARAGRAPH STRUCTURE")
    print(f"  Paragraphs:        {first_para['paragraph_count']} → {final_para['paragraph_count']}")
    print(f"  Avg sentences/para: {first_para['avg_sentences_per_paragraph']} → {final_para['avg_sentences_per_paragraph']}")
    print(f"  Avg first-sent words: {first_para['avg_first_sentence_words']} → {final_para['avg_first_sentence_words']} (topic sentence weight)")
    print(f"  Avg last-sent words:  {first_para['avg_last_sentence_words']} → {final_para['avg_last_sentence_words']} (landing weight)")
    print(f"  Single-sentence paras: {first_para['short_paragraph_count']} → {final_para['short_paragraph_count']}")
    print(f"  Long paras (5+ sents): {first_para['long_paragraph_count']} → {final_para['long_paragraph_count']}")

    print(f"\n  COHESION (sentence-to-sentence lexical chain density)")
    print(f"  Mean adjacency overlap: {first_coh['mean_adjacency_overlap']} → {final_coh['mean_adjacency_overlap']}")
    print(f"  Cohesion score (0-10):  {first_coh['cohesion_score']} → {final_coh['cohesion_score']}")
    print(f"  Low-cohesion pairs:     {first_coh['low_cohesion_pair_count']} → {final_coh['low_cohesion_pair_count']}")
    if final_coh['low_cohesion_pairs']:
        print(f"\n  Final-draft cohesion breaks (low overlap with prior sentence):")
        for p in final_coh['low_cohesion_pairs'][:3]:
            print(f"    overlap={p['overlap']}")
            print(f"      [prior]: {p['sent1_preview']}")
            print(f"      [next]:  {p['sent2_preview']}")

    # --- Profile update (skip in --quantitative mode) ---
    if update_profile:
        # Save updated profile — write back only user-profile fields, not merged base data.
        # If the profile was a base+user merge, _user_profile_path points to the user file.
        # If it's a standalone profile, profile_path is used directly.
        write_path = updated.get("_user_profile_path", profile_path)

        # Reload the user-only profile from disk to avoid writing base data into user file
        with open(write_path, "r", encoding="utf-8") as f:
            user_only = json.load(f)

        # Copy updated computational sections back into user-only profile
        for key in ("stylometry", "perplexity", "embeddings"):
            if key in updated:
                user_only[key] = updated[key]

        # If genre/voice separation ran (or genre bootstrap), persist the
        # genre stylometry block into the user-only profile too.
        applied_genre = updated.get("_genre_separation_applied")
        if applied_genre and "genres" in updated:
            user_only.setdefault("genres", {})
            updated_genre_block = updated["genres"].get(applied_genre, {}) or {}
            existing_genre_block = user_only["genres"].get(applied_genre, {}) or {}
            # Preserve everything in the existing genre block (description,
            # word_count_target, threshold_overrides, genre_moves, qualitative,
            # ...); only refresh the stylometry sub-block.
            merged_genre_block = dict(existing_genre_block)
            if isinstance(updated_genre_block, dict) and "stylometry" in updated_genre_block:
                merged_genre_block["stylometry"] = updated_genre_block["stylometry"]
            # If the existing block is empty (genre is new), carry over
            # the description seed we set above.
            if not merged_genre_block.get("description") and updated_genre_block.get("description"):
                merged_genre_block["description"] = updated_genre_block["description"]
            user_only["genres"][applied_genre] = merged_genre_block

        with open(write_path, "w", encoding="utf-8") as f:
            json.dump(user_only, f, indent=2, ensure_ascii=False)

        revision_count = updated["stylometry"]["revision_count"]
        print(f"\n  Profile updated. Revision count: {revision_count}")
        notes_preview = updated["stylometry"].get("style_notes", "")[:160]
        if notes_preview:
            print(f"  Style notes: {notes_preview}...")
        if applied_genre:
            g_count = (updated.get("genres", {})
                              .get(applied_genre, {})
                              .get("stylometry", {})
                              .get("revision_count", 0))
            print(f"  Genre '{applied_genre}' centroid revision count: {g_count}")
    else:
        print(f"\n  (--quantitative mode: profile NOT updated)")

    # --- Phase 4: Qualitative analysis prompt ---
    print(f"\n{sep}")
    print("  QUALITATIVE ANALYSIS REQUIRED")
    print(sep)
    print("""
  Agent: read both draft files in full and the diff above, then perform a
  CDA sweep at each level. The quantitative update only captures surface
  metrics; the qualitative analysis is where the actual learning happens.

  CLAUSE / SENTENCE LEVEL
  □ Transitivity: were material processes ('I built', 'I traced') substituted
    for relational ('this is', 'these are')? Or vice versa?
  □ Modality: were epistemic hedges added or removed (might, could, appears)?
  □ Nominalization: were verb forms converted to nouns or back? Less is
    generally clearer, UNLESS the nominal form is an established academic
    concept the audience already holds, or denominalization would confuse.
  □ Given/new flow: does each revised sentence's subject pick up from the
    prior sentence's new information? Flag adjacent sentences with no shared
    referent — these are cohesion breaks (see metrics above).
  □ Jargon precision: were imprecise theory labels (apparatus, recognition,
    dispositif) replaced with more specific mechanisms? Or vice versa where
    the term was load-bearing shorthand?

  PARAGRAPH LEVEL
  □ Topic sentence position: did revisions move claims to sentence-initial?
  □ Evidence structure: did body sentences become more specific/grounded?
  □ Landing weight: did paragraph endings gain rhetorical force?
  □ One-focus discipline: were over-loaded paragraphs split or refocused?

  DOCUMENT LEVEL
  □ Structural reorganization: paragraphs reordered? (see paragraph moves)
  □ Arc: did the argument's overall shape change, or just the prose?
  □ Synthesis moves: do connections move 'upward and outward' (these threads
    open new territory together) rather than 'inward' (these are all examples
    of the same pattern)?

  PROFILE ACTIONS
  □ **Editorial discipline: the profile should sharpen with each loop, not grow. Treat addition as the option of last resort, after rephrase and merge are ruled out.**
  □ Map each major change type to existing qualitative checks. Which checks predicted the change? (signals they're working.)
  □ What is the smallest set of profile changes — additions, deletions, merges, or rephrasings — that would have caught the deliberate revision moves? Consider each lens:
      • REPHRASE: did an existing check fire weakly because its instruction is imprecise? Sharpen the language.
      • MERGE: did two or more checks point at the same concern from different angles? Collapse them, absorbing distinctive language.
      • ROLE-REASSIGN or CUT: was a check tagged `pre_draft` that didn't actually shape this revision? Demote to `diagnostic`, or cut.
      • ADD: is there a genuinely new pattern not covered? Specify role at insertion (pre_draft / linter / cda_sweep / diagnostic). If `pre_draft`, name what existing pre_draft check it replaces — the in-flight set is capped, additions force tradeoffs.
      • CUT (silence): are there checks that haven't fired across this or the last several revisions? Flag for next audit.
  □ For accepted additions and significant rephrasings, append an entry to `~/.claude/skills/voice-check/PROFILE_CHANGE_LOG.md`: source diff snippet (quoted, not summarized) + rationale + role + a question for the next audit. Merges and cuts don't require log entries (they reorganize existing rationale rather than create new). This preserves the *why* against rationale drift, separately from the citation log's tracking of *whether the check is still firing*.
  □ Present proposed changes to the user for approval before updating.

  WORKFLOW NOTE
  □ If this revision was a structural pass (see diff pattern above), weight
    sentence-level signals lower — they often reflect collateral damage from
    reorganization, not deliberate voice choices. The reverse is also true:
    fine-grained refinement passes carry the strongest voice signal at the
    sentence level.
""")

    # --- Citation tracking + DIAGNOSTIC REVIEW auto-trigger ---
    # Scan the diff report (which surfaces actual revision text) plus the
    # user's notes for any check ID citations. Append to citation_log.json
    # and surface DIAGNOSTIC REVIEW DUE if any diagnostic check has been
    # silent for DIAGNOSTIC_SILENCE_THRESHOLD runs.
    scan_text = (diff_report_str or "") + " " + (notes or "")
    emit_cited_checks_and_update_log(
        scanned_text=scan_text,
        profile=profile,
        command="--learn",
        files=[os.path.basename(first_draft_path), os.path.basename(final_draft_path)],
    )


# ---------------------------------------------------------------------------
# Multi-version learning loop (--learn-sequence)
# ---------------------------------------------------------------------------

def _classify_transition_auto(diff_result: dict) -> str:
    """
    Auto-classify a transition between two consecutive versions as
    'structural', 'fine-grained', or 'mixed'.

    Heuristic:
      - structural: change_rate >50% AND structural pattern (paragraph moves)
      - fine-grained: change_rate <30% OR pattern is 'local' with low change rate
      - mixed: in between

    Errs on the side of 'structural' for ambiguous cases — safer to skip than
    over-weight a structural pair into the EMA.
    """
    change_rate = diff_result.get("change_rate", 0.0)
    pattern = diff_result.get("structural_vs_local", "structural")

    # Strong structural signal: >50% changed AND structural pattern detected.
    if change_rate > 50 and pattern == "structural":
        return "structural"
    # Strong structural signal: very high change rate even without paragraph
    # moves likely indicates large rewrites — treat as structural.
    if change_rate > 60:
        return "structural"
    # Strong fine-grained signal: low change rate AND local pattern.
    if change_rate < 30 and pattern == "local":
        return "fine-grained"
    # Local pattern with somewhat higher change rate is still mostly
    # sentence-level — but be conservative and call this mixed.
    if pattern == "local" and change_rate < 40:
        return "fine-grained"
    # Pure structural pattern at lower change rate is still architectural.
    if pattern == "structural":
        return "structural"
    # Fallback: ambiguous middle band.
    return "mixed"


def _filename_to_version_token(name: str) -> str:
    """
    Reduce a filename like 'APPLICATION_DRAFT_V14.md' to a normalized token
    'v14' for lenient manifest matching. Returns lowercased basename without
    extension if no version pattern is detected.
    """
    base = os.path.basename(name)
    base_no_ext = os.path.splitext(base)[0]
    # Look for 'V' or 'v' followed by digits (with optional letter suffix like 13b)
    m = re.search(r"[Vv](\d+[a-zA-Z]?)", base_no_ext)
    if m:
        return "v" + m.group(1).lower()
    # Common case: APPLICATION_DRAFT.md is treated as v3 (matching the user's
    # convention that the unsuffixed file is the earliest version in scope).
    # We don't hard-code this — return the bare lowercased stem instead and
    # let manifest matching be lenient.
    return base_no_ext.lower()


def parse_version_manifest(manifest_path: str) -> dict:
    """
    Parse a VERSION_MANIFEST.md file. Returns a dict keyed by
    (from_token, to_token) -> {'type': str, 'author': str, 'notes': str}.

    Expected table format:
        | From | To | Type | Author | Notes |
        |------|-----|------|--------|-------|
        | v3 | v4 | structural | AI | ... |
        | v5 | v6 | fine-grained | user | ... |

    Tolerates extra whitespace, missing columns, and varying column order.
    """
    classifications = {}
    if not manifest_path or not os.path.isfile(manifest_path):
        return classifications

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return classifications

    # Find table rows: lines that start with | and contain at least 3 |s
    row_re = re.compile(r"^\s*\|(.+)\|\s*$")
    sep_re = re.compile(r"^\s*\|[\s\-:|]+\|\s*$")

    rows = []
    for line in content.splitlines():
        if sep_re.match(line):
            continue
        m = row_re.match(line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if len(cells) < 3:
            continue
        rows.append(cells)

    if not rows:
        return classifications

    # First row should be header; locate column indices for From, To, Type.
    header = [h.lower() for h in rows[0]]
    try:
        from_idx = header.index("from")
        to_idx = header.index("to")
        type_idx = header.index("type")
    except ValueError:
        # Fall back to fixed positions
        from_idx, to_idx, type_idx = 0, 1, 2

    author_idx = None
    notes_idx = None
    for i, h in enumerate(header):
        if h == "author":
            author_idx = i
        elif h in ("notes", "intent", "note"):
            notes_idx = i

    for cells in rows[1:]:
        if max(from_idx, to_idx, type_idx) >= len(cells):
            continue
        from_tok = cells[from_idx].lower().strip()
        to_tok = cells[to_idx].lower().strip()
        ttype = cells[type_idx].lower().strip()
        # Normalize 'fine grained', 'fine_grained' -> 'fine-grained'
        ttype = ttype.replace("_", "-").replace(" ", "-")
        if ttype not in ("structural", "fine-grained", "mixed"):
            # Unknown classification — skip rather than guess
            continue
        author = cells[author_idx].strip() if author_idx is not None and author_idx < len(cells) else ""
        notes = cells[notes_idx].strip() if notes_idx is not None and notes_idx < len(cells) else ""
        classifications[(from_tok, to_tok)] = {
            "type": ttype,
            "author": author,
            "notes": notes,
        }
    return classifications


def _lookup_manifest_classification(manifest: dict, from_path: str, to_path: str):
    """
    Look up a manifest classification for a pair of file paths. Returns the
    classification dict, or None if no match. Lenient: matches tokens like
    'v3' against 'APPLICATION_DRAFT_V3.md'.
    """
    if not manifest:
        return None
    from_tok = _filename_to_version_token(from_path)
    to_tok = _filename_to_version_token(to_path)
    # Exact token match
    if (from_tok, to_tok) in manifest:
        return manifest[(from_tok, to_tok)]
    # Fall back: try matching on stem against any manifest token whose value
    # is a prefix of the filename
    from_base = os.path.splitext(os.path.basename(from_path))[0].lower()
    to_base = os.path.splitext(os.path.basename(to_path))[0].lower()
    for (mf, mt), val in manifest.items():
        if (mf in from_base or from_base.endswith(mf)) and (mt in to_base or to_base.endswith(mt)):
            return val
    return None


def _select_pairs_for_update(transitions: list, cap: int = 4) -> list:
    """
    Given a list of transition dicts (each with 'classification' key, in
    sequence order), select up to `cap` fine-grained pairs sampled evenly
    across the refinement phase.

    If <= cap fine-grained pairs exist, return them all. If more, sample
    first, last, and (cap - 2) interior points evenly spaced.
    """
    fine = [t for t in transitions if t["classification"] == "fine-grained"]
    if len(fine) <= cap:
        return fine
    # Even sampling: indices 0, last, and interior points
    n = len(fine)
    if cap <= 1:
        return [fine[0]]
    if cap == 2:
        return [fine[0], fine[-1]]
    indices = [0]
    interior_count = cap - 2
    if interior_count > 0:
        # Evenly spaced interior indices in (0, n-1)
        step = (n - 1) / (interior_count + 1)
        for k in range(1, interior_count + 1):
            idx = int(round(k * step))
            if idx <= 0:
                idx = 1
            if idx >= n - 1:
                idx = n - 2
            indices.append(idx)
    indices.append(n - 1)
    # De-duplicate while preserving order
    seen = set()
    unique = []
    for i in indices:
        if i not in seen:
            seen.add(i)
            unique.append(i)
    return [fine[i] for i in unique]


def _detect_phase_transition(transitions: list, window: int = 3):
    """
    Detect the index where the running classification flips from
    majority-structural to majority-fine-grained over a sliding window of
    `window` consecutive pairs. Returns the transition dict at the flip
    point, or None if no clean flip is detected.
    """
    if len(transitions) < window:
        return None

    def majority(group):
        struct = sum(1 for t in group if t["classification"] == "structural")
        fine = sum(1 for t in group if t["classification"] == "fine-grained")
        if struct > fine:
            return "structural"
        if fine > struct:
            return "fine-grained"
        return "mixed"

    # Walk windows; find first flip from structural-majority to fine-majority
    prev_majority = None
    for i in range(len(transitions) - window + 1):
        group = transitions[i:i + window]
        maj = majority(group)
        if prev_majority == "structural" and maj == "fine-grained":
            # Flip happened within this window — call the first fine-grained
            # pair in the window the transition point.
            for t in group:
                if t["classification"] == "fine-grained":
                    return t
            return group[0]
        if maj in ("structural", "fine-grained"):
            prev_majority = maj
    return None


def learn_from_sequence(
    file_paths: list,
    profile_path: str,
    genre: str = None,
    manifest_path: str = None,
    dry_run: bool = False,
    notes: str = "",
):
    """
    Multi-version learning loop. Iterates over consecutive pairs in
    file_paths, classifies each transition as structural / fine-grained /
    mixed, and applies EMA updates only on fine-grained pairs (capped to
    avoid over-weighting one application).

    Algorithm (see module docs for full spec):
      1. Read all files.
      2. For each consecutive pair, run diff_analysis.compute_diff and
         classify (manifest override > auto-classify).
      3. Detect phase transition (sliding window majority flip).
      4. Select up to 4 fine-grained pairs (sampled evenly).
      5. If not dry_run, call learn_from_revision on each selected pair.
      6. Print a revision trajectory report.
    """
    try:
        from diff_analysis import compute_diff
    except ImportError:
        print("Error: diff_analysis.py not found. Cannot run --learn-sequence.",
              file=sys.stderr)
        sys.exit(1)

    if len(file_paths) < 2:
        print("Error: --learn-sequence requires at least 2 files.", file=sys.stderr)
        sys.exit(1)

    # Verify all files exist
    for p in file_paths:
        if not os.path.isfile(p):
            print(f"Error: File not found: {p}", file=sys.stderr)
            sys.exit(1)
    if not os.path.isfile(profile_path):
        print(f"Error: Profile not found: {profile_path}", file=sys.stderr)
        sys.exit(1)

    # Parse manifest (may be empty)
    manifest = parse_version_manifest(manifest_path) if manifest_path else {}
    if manifest_path and not manifest:
        print(f"  Warning: manifest at {manifest_path} produced no usable rows; "
              f"falling back to auto-classification.", file=sys.stderr)

    # Read all texts
    texts = []
    for p in file_paths:
        with open(p, "r", encoding="utf-8") as fh:
            texts.append(fh.read())

    # Build transitions
    transitions = []
    for i in range(len(file_paths) - 1):
        from_path = file_paths[i]
        to_path = file_paths[i + 1]
        from_label = _filename_to_version_token(from_path)
        to_label = _filename_to_version_token(to_path)
        diff = compute_diff(texts[i], texts[i + 1])

        manifest_hit = _lookup_manifest_classification(manifest, from_path, to_path)
        if manifest_hit is not None:
            classification = manifest_hit["type"]
            source = "manifest"
        else:
            classification = _classify_transition_auto(diff)
            source = "auto"

        transitions.append({
            "index": i,
            "from_path": from_path,
            "to_path": to_path,
            "from_label": from_label,
            "to_label": to_label,
            "diff": diff,
            "classification": classification,
            "classification_source": source,
            "manifest_entry": manifest_hit,
        })

    # Detect phase transition
    phase_transition = _detect_phase_transition(transitions)

    # Select pairs for update
    selected = _select_pairs_for_update(transitions, cap=4)

    # Cohesion trajectory: compute first and final cohesion scores for context
    try:
        first_cohesion = analyze_cohesion(texts[0]).get("cohesion_score", None)
        last_cohesion = analyze_cohesion(texts[-1]).get("cohesion_score", None)
    except Exception:
        first_cohesion = None
        last_cohesion = None

    # ---- Print trajectory report ----
    sep = "═" * 51
    print(f"\n{sep}")
    print("  REVISION TRAJECTORY")
    print(sep)

    first_label = _filename_to_version_token(file_paths[0])
    last_label = _filename_to_version_token(file_paths[-1])
    print(f"\n  Sequence: {len(file_paths)} versions ({first_label} → {last_label})")
    print(f"  Profile: {os.path.basename(profile_path)}")
    print(f"  Genre: {genre if genre else 'none'}")
    print(f"  Mode: {'dry-run' if dry_run else 'full'}")
    if notes:
        print(f"  Notes: {notes}")
    if manifest_path:
        if manifest:
            print(f"  Manifest: {os.path.basename(manifest_path)} ({len(manifest)} rows)")
        else:
            print(f"  Manifest: {os.path.basename(manifest_path)} (unparsed, using auto-classification)")

    # Transition classifications
    print(f"\n  TRANSITION CLASSIFICATIONS")
    for t in transitions:
        diff = t["diff"]
        cr = diff.get("change_rate", 0.0)
        first_paras = diff.get("first_paragraph_count", "?")
        final_paras = diff.get("final_paragraph_count", "?")
        pattern = diff.get("structural_vs_local", "?")
        cls_label = t["classification"].upper()
        src_marker = " (manifest)" if t["classification_source"] == "manifest" else ""
        pair_label = f"{t['from_label']} → {t['to_label']}"
        # Pad label for alignment
        print(
            f"    {pair_label:<20} [{cls_label:<13}]{src_marker} "
            f"change_rate {cr}%, paragraphs {first_paras}→{final_paras}, "
            f"{pattern} pattern"
        )

    # Phase transition
    print(f"\n  PHASE TRANSITION")
    if phase_transition is not None:
        pt_idx = phase_transition["index"]
        pt_label = f"{phase_transition['from_label']} → {phase_transition['to_label']}"
        print(f"    Detected at {pt_label}: shift from structural exploration to refinement.")
        # Phase boundaries
        struct_pairs = transitions[:pt_idx]
        refine_pairs = transitions[pt_idx:]
        if struct_pairs:
            sp_first = struct_pairs[0]["from_label"]
            sp_last = struct_pairs[-1]["to_label"]
            print(f"    Structural phase: {sp_first}–{sp_last} ({len(struct_pairs)} pairs)")
        else:
            print(f"    Structural phase: (none — refinement starts at first transition)")
        if refine_pairs:
            rp_first = refine_pairs[0]["from_label"]
            rp_last = refine_pairs[-1]["to_label"]
            print(f"    Refinement phase: {rp_first}–{rp_last} ({len(refine_pairs)} pairs)")
    else:
        print(f"    No clean phase transition detected (sequence may be all structural, "
              f"all fine-grained, or too short).")

    # Selected pairs
    fine_count = sum(1 for t in transitions if t["classification"] == "fine-grained")
    print(f"\n  SELECTED PAIRS FOR LEARNING UPDATE")
    if not selected:
        print(f"    (none — no fine-grained transitions found)")
    else:
        # Annotate each selected pair with its position in the fine-grained sub-list
        fine_list = [t for t in transitions if t["classification"] == "fine-grained"]
        total_fine = len(fine_list)
        for t in selected:
            try:
                fi = fine_list.index(t)
            except ValueError:
                fi = -1
            if total_fine == 1:
                annot = "only fine-grained pair"
            elif fi == 0:
                annot = "fine-grained, first refinement"
            elif fi == total_fine - 1:
                annot = "fine-grained, final"
            else:
                annot = "fine-grained, mid-refinement"
            pair_label = f"{t['from_label']} → {t['to_label']}"
            print(f"    [✓] {pair_label:<20} ({annot})")
        print(f"    Total: {len(selected)} pairs (out of {fine_count} fine-grained; "
              f"{'all included' if len(selected) == fine_count else 'sampled across refinement'})")

    # Cohesion trajectory
    print(f"\n  COHESION TRAJECTORY")
    if first_cohesion is not None and last_cohesion is not None:
        delta_word = "improved" if last_cohesion > first_cohesion else (
            "decreased" if last_cohesion < first_cohesion else "unchanged"
        )
        print(f"    First version cohesion score: {first_cohesion}")
        print(f"    Final version cohesion score: {last_cohesion} ({delta_word})")
    else:
        print(f"    (cohesion metric unavailable)")

    # Profile updates
    print(f"\n  PROFILE UPDATE")
    if dry_run:
        print(f"    --dry-run: profile NOT modified. {len(selected)} fine-grained "
              f"pair(s) WOULD be applied.")
    elif not selected:
        print(f"    No fine-grained pairs selected; profile not modified.")
    else:
        print(f"    Applying {len(selected)} fine-grained pair(s) to profile via EMA "
              f"(through learn_from_revision).")
        for t in selected:
            pair_label = f"{t['from_label']} → {t['to_label']}"
            sub_notes = notes or ""
            seq_tag = f"[--learn-sequence pair {pair_label}]"
            combined_notes = (sub_notes + " " + seq_tag).strip()
            try:
                learn_from_revision(
                    t["from_path"], t["to_path"], profile_path,
                    notes=combined_notes,
                    update_profile=True,
                    genre=genre,
                )
            except SystemExit:
                # learn_from_revision sys.exits on missing modules; re-raise
                raise
            except Exception as e:
                print(f"    Error updating profile for pair {pair_label}: {e}",
                      file=sys.stderr)

    # Qualitative analysis prompt
    print(f"\n{sep}")
    print("  QUALITATIVE ANALYSIS REQUIRED")
    print(sep)
    print("""
  Agent: read the refinement-phase versions and perform CDA sweep.
  Focus on the SELECTED PAIRS above — those carry the highest voice signal.
  Sentence-level changes in the structural phase often reflect collateral
  damage from reorganization, not deliberate voice choices; weight them
  lower in qualitative analysis.

  □ Read each selected pair (FROM and TO) in full.
  □ Identify clause/sentence-level moves the human made deliberately.
  PROFILE ACTIONS
  □ **Editorial discipline: the profile should sharpen with each loop, not grow. Treat addition as the option of last resort, after rephrase and merge are ruled out.**
  □ Map each major change type to existing qualitative checks. Which checks predicted the change? (signals they're working.)
  □ What is the smallest set of profile changes — additions, deletions, merges, or rephrasings — that would have caught the deliberate revision moves? Consider each lens:
      • REPHRASE: did an existing check fire weakly because its instruction is imprecise? Sharpen the language.
      • MERGE: did two or more checks point at the same concern from different angles? Collapse them, absorbing distinctive language.
      • ROLE-REASSIGN or CUT: was a check tagged `pre_draft` that didn't actually shape this revision? Demote to `diagnostic`, or cut.
      • ADD: is there a genuinely new pattern not covered? Specify role at insertion (pre_draft / linter / cda_sweep / diagnostic). If `pre_draft`, name what existing pre_draft check it replaces — the in-flight set is capped, additions force tradeoffs.
      • CUT (silence): are there checks that haven't fired across this or the last several revisions? Flag for next audit.
  □ For accepted additions and significant rephrasings, append an entry to `~/.claude/skills/voice-check/PROFILE_CHANGE_LOG.md`: source diff snippet (quoted, not summarized) + rationale + role + a question for the next audit. Merges and cuts don't require log entries (they reorganize existing rationale rather than create new). This preserves the *why* against rationale drift, separately from the citation log's tracking of *whether the check is still firing*.
  □ Present proposed changes to the user for approval before updating.
""")

    # --- Citation tracking + DIAGNOSTIC REVIEW auto-trigger ---
    profile_for_scan = load_profile(profile_path)
    # Scan transition labels and notes — the per-transition diff strings
    # aren't easily reassembled here, but the citation log entry is still
    # valuable as a heartbeat for diagnostic-silence tracking.
    scan_parts = [notes or ""]
    for t in transitions:
        scan_parts.append(f"{t.get('from_label','')} {t.get('to_label','')} {t.get('classification','')}")
    scan_text = " ".join(scan_parts)
    emit_cited_checks_and_update_log(
        scanned_text=scan_text,
        profile=profile_for_scan,
        command="--learn-sequence" + (" --dry-run" if dry_run else ""),
        files=[os.path.basename(p) for p in file_paths],
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_analysis(filepath: str, target: int = 1200) -> dict:
    raw_lines, analysis_text, body_lines, body_line_map, header_count = load_and_prepare(filepath)

    # Edge case: empty or headers-only files
    stripped = analysis_text.strip()
    if not stripped:
        return {
            "file": os.path.basename(filepath),
            "file_path": filepath,
            "headers_stripped": header_count,
            "words": {"total": 0, "target": target, "pct_diff": -100.0, "flag": False},
            "sentences": {"count": 0, "avg_length": 0, "max_length": 0,
                          "long_threshold": THRESH_LONG_SENT,
                          "rewrite_threshold": THRESH_REWRITE_SENT,
                          "over_long_count": 0, "over_rewrite_count": 0,
                          "over_long": [], "over_rewrite": [],
                          "flag_long": False, "flag_rewrite": False},
            "emdashes": {"total": 0, "per_1000": 0, "long_insertions": [],
                         "flag_density": False, "flag_insertions": False},
            "hedges": {"count": 0, "items": [], "flag": False},
            "aggrandizing": {"count": 0, "items": [], "flag": False},
            "topic_sentences": {"count": 0, "items": [], "flag": False},
            "passive": {"count": 0, "examples": []},
            "connectors": {"count": 0, "items": [], "flag": False},
            "readability": {"flesch_kincaid": 0, "gunning_fog": 0, "flesch_reading_ease": 0},
            "padding": {"count": 0, "items": [], "flag": False},
            "product_descriptions": {"count": 0, "items": [], "flag": False},
            "front_loading": {"heavy_subject_count": 0, "heavy_subject_max": 0,
                              "examples": [], "flag": False},
            "flagged_sentences": [],
            "empty": True,
        }

    word_data = analyze_words(analysis_text, target)

    results = {
        "file": os.path.basename(filepath),
        "file_path": filepath,
        "headers_stripped": header_count,
        "words": word_data,
        "sentences": analyze_sentences(analysis_text),
        "emdashes": analyze_emdashes(analysis_text, word_data["total"], raw_lines, body_lines, body_line_map),
        "hedges": analyze_hedges(analysis_text, raw_lines, body_lines, body_line_map),
        "aggrandizing": analyze_aggrandizing(analysis_text, raw_lines, body_lines, body_line_map),
        "topic_sentences": analyze_topic_sentences(analysis_text, raw_lines, body_lines, body_line_map),
        "passive": analyze_passive_voice(analysis_text),
        "connectors": analyze_connectors(analysis_text, raw_lines, body_lines, body_line_map),
        "readability": analyze_readability(analysis_text),
        "padding": analyze_padding(analysis_text, raw_lines, body_lines, body_line_map),
        "product_descriptions": analyze_product_descriptions(analysis_text, raw_lines, body_lines, body_line_map),
        "corporate_jargon": analyze_corporate_jargon(analysis_text, raw_lines, body_lines, body_line_map),
        "front_loading": analyze_front_loading(analysis_text, raw_lines, body_lines, body_line_map),
    }

    flagged = collect_flagged_sentences(analysis_text, raw_lines, body_lines, body_line_map, results)
    results["flagged_sentences"] = flagged

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Voicing analysis for draft documents. Supports configurable voice profiles."
    )
    parser.add_argument("file", nargs="?", help="Path to the draft file to analyze")
    parser.add_argument(
        "--target", type=int, default=None,
        help="Target word count (default: 1200, or genre target if --genre specified)"
    )
    parser.add_argument(
        "--json", action="store_true", dest="output_json",
        help="Output JSON instead of formatted report"
    )
    parser.add_argument(
        "--profile", type=str, default=None,
        help="Path to a voice profile JSON file"
    )
    parser.add_argument(
        "--calibrate", type=str, default=None, metavar="SAMPLE_DIR",
        help="Analyze writing samples in SAMPLE_DIR and generate a voice profile"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None,
        help="Output path for generated profile (used with --calibrate)"
    )
    parser.add_argument(
        "--genre", type=str, default=None,
        help="Genre for threshold selection (e.g., research_paper, academic_position). "
             "Uses genre-specific threshold overrides and word count target from profile."
    )
    parser.add_argument(
        "--learn", nargs=2, metavar=("FIRST_DRAFT", "FINAL_DRAFT"),
        help="Full learning loop — diff analysis + quantitative update + qualitative analysis prompt"
    )
    parser.add_argument(
        "--quantitative", nargs=2, metavar=("FIRST_DRAFT", "FINAL_DRAFT"),
        help="Quantitative comparison only (deltas, no profile update, no qualitative prompt)"
    )
    parser.add_argument(
        "--diff", nargs=2, metavar=("FIRST_DRAFT", "FINAL_DRAFT"),
        help="Structural diff only — sentence change classification + paragraph reorder detection"
    )
    parser.add_argument(
        "--notes", type=str, default="",
        help="Intent note for --learn run (e.g., 'structural pass', 'fine-grained finalization')"
    )
    parser.add_argument(
        "--learn-sequence", nargs="*", metavar="FILE", dest="learn_sequence", default=None,
        help="Multi-version learning loop. Pass 2+ files in revision order; auto-classifies each "
             "transition as structural or fine-grained, applies EMA updates only on fine-grained pairs. "
             "May be combined with --auto-discover (in which case the file list is supplied implicitly)."
    )
    parser.add_argument(
        "--manifest", type=str, default=None,
        help="Optional path to a VERSION_MANIFEST.md that explicitly tags transitions "
             "(overrides auto-classification)"
    )
    parser.add_argument(
        "--auto-discover", type=str, default=None, metavar="DIR", dest="auto_discover",
        help="With --learn-sequence: auto-discover .md files in DIR matching --pattern, "
             "sorted by --sort-by"
    )
    parser.add_argument(
        "--pattern", type=str, default="*.md",
        help="Glob pattern for --auto-discover (default: *.md)"
    )
    parser.add_argument(
        "--sort-by", type=str, default="name", choices=["name", "mtime"], dest="sort_by",
        help="Sort order for --auto-discover (default: name)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", dest="dry_run",
        help="With --learn-sequence: report classifications and what WOULD be updated, "
             "without writing to profile"
    )
    parser.add_argument(
        "--audit-diagnostics", action="store_true", dest="audit_diagnostics",
        help="Read-only report on diagnostic-role checks: last-cited dates, "
             "citation counts. Auto-triggered when a diagnostic check has been "
             "silent for 5+ runs."
    )
    parser.add_argument(
        "--log-cited-checks", type=str, dest="log_cited_checks", default=None,
        help="Comma-separated check IDs to append to the most recent run's "
             "citation log entry. Called by agents after Phase 4 CDA sweep "
             "to record which checks fired during revision."
    )
    args = parser.parse_args()

    # Audit diagnostics mode (no draft file required)
    if args.audit_diagnostics:
        run_audit_diagnostics(profile_path=args.profile)
        return

    # Post-analysis citation logging (no draft file required)
    if args.log_cited_checks:
        ids = [s.strip() for s in args.log_cited_checks.split(",") if s.strip()]
        if not ids:
            print("Error: --log-cited-checks requires at least one ID", file=sys.stderr)
            sys.exit(1)
        log_cited_checks_postanalysis(ids, profile_path=args.profile)
        return

    # Diff-only mode (no profile required)
    if args.diff:
        try:
            from diff_analysis import compute_diff, format_diff_report
        except ImportError:
            print("Error: diff_analysis.py not found.", file=sys.stderr)
            sys.exit(1)
        first_path, final_path = args.diff
        for p in (first_path, final_path):
            if not os.path.isfile(p):
                print(f"Error: File not found: {p}", file=sys.stderr)
                sys.exit(1)
        with open(first_path) as f:
            first_text = f.read()
        with open(final_path) as f:
            final_text = f.read()
        diff = compute_diff(first_text, final_text)
        print(format_diff_report(diff))
        return

    # Multi-version learning mode (--learn-sequence)
    if args.learn_sequence is not None or args.auto_discover:
        # Auto-discover replaces explicit file list
        file_paths = list(args.learn_sequence) if args.learn_sequence else []
        if args.auto_discover:
            import glob
            if not os.path.isdir(args.auto_discover):
                print(f"Error: --auto-discover directory not found: {args.auto_discover}",
                      file=sys.stderr)
                sys.exit(1)
            pattern_path = os.path.join(args.auto_discover, args.pattern)
            discovered = glob.glob(pattern_path)
            if not discovered:
                print(f"Error: No files matched {pattern_path}", file=sys.stderr)
                sys.exit(1)
            if args.sort_by == "mtime":
                discovered.sort(key=lambda p: os.path.getmtime(p))
            else:
                # Natural-ish sort: split into (text, number) chunks so V2 < V10
                def natkey(s):
                    return [int(c) if c.isdigit() else c.lower()
                            for c in re.split(r"(\d+)", os.path.basename(s))]
                discovered.sort(key=natkey)
            file_paths = discovered
            print(f"  Auto-discovered {len(file_paths)} files in {args.auto_discover}",
                  file=sys.stderr)

        if len(file_paths) < 2:
            parser.error("--learn-sequence requires at least 2 files (after --auto-discover)")

        # Resolve profile (same logic as --learn)
        if not args.profile:
            discovered_path, count = discover_profile()
            if discovered_path:
                print(f"  Auto-discovered profile: {os.path.basename(discovered_path)}",
                      file=sys.stderr)
                args.profile = discovered_path
            elif count > 1:
                profiles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles")
                available = sorted(
                    f for f in os.listdir(profiles_dir)
                    if f.endswith(".json") and f != "base.json"
                )
                print("Multiple profiles found. Use --profile to specify:", file=sys.stderr)
                for p in available:
                    print(f"  --profile profiles/{p}", file=sys.stderr)
                sys.exit(1)
            else:
                parser.error("--learn-sequence requires --profile (no user profile found; "
                             "run --calibrate first)")

        learn_from_sequence(
            file_paths,
            profile_path=args.profile,
            genre=args.genre,
            manifest_path=args.manifest,
            dry_run=args.dry_run,
            notes=args.notes,
        )
        return

    # Learning mode (full pipeline) OR quantitative-only mode
    learn_args = args.learn or args.quantitative
    if learn_args:
        update_profile = bool(args.learn)  # --learn updates; --quantitative does not
        if not args.profile:
            # Try auto-discovery before failing
            discovered_path, count = discover_profile()
            if discovered_path:
                print(f"  Auto-discovered profile: {os.path.basename(discovered_path)}",
                      file=sys.stderr)
                args.profile = discovered_path
            elif count > 1:
                profiles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles")
                available = sorted(
                    f for f in os.listdir(profiles_dir)
                    if f.endswith(".json") and f != "base.json"
                )
                print("Multiple profiles found. Use --profile to specify:", file=sys.stderr)
                for p in available:
                    print(f"  --profile profiles/{p}", file=sys.stderr)
                sys.exit(1)
            else:
                parser.error("--learn/--quantitative requires --profile (no user profile found; run --calibrate first)")
        first_path, final_path = learn_args
        for p in (first_path, final_path):
            if not os.path.isfile(p):
                print(f"Error: File not found: {p}", file=sys.stderr)
                sys.exit(1)
        if not os.path.isfile(args.profile):
            print(f"Error: Profile not found: {args.profile}", file=sys.stderr)
            sys.exit(1)
        learn_from_revision(first_path, final_path, args.profile,
                            notes=args.notes, update_profile=update_profile,
                            genre=args.genre)
        return

    # Calibration mode
    if args.calibrate:
        if not os.path.isdir(args.calibrate):
            print(f"Error: Directory not found: {args.calibrate}", file=sys.stderr)
            sys.exit(1)
        # If --genre is specified for calibration, --output must point at an
        # existing profile to merge into. Resolve a sensible default if user
        # didn't pass --output explicitly.
        out_path = args.output
        if args.genre and not out_path:
            discovered, count = discover_profile()
            if discovered:
                out_path = discovered
                print(f"  --calibrate --genre {args.genre}: writing into "
                      f"discovered profile {os.path.basename(out_path)}",
                      file=sys.stderr)
            else:
                print("Error: --calibrate --genre requires --output to point at "
                      "an existing user profile, or exactly one user profile in "
                      "the profiles/ directory for auto-discovery.", file=sys.stderr)
                sys.exit(1)
        calibrate_from_samples(args.calibrate, out_path, genre=args.genre)
        return

    # Analysis mode — file is required
    if not args.file:
        parser.error("the following arguments are required: file (or use --calibrate)")

    if not os.path.isfile(args.file):
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    # Auto-discover profile if not specified
    if args.profile is None:
        discovered_path, count = discover_profile()
        if discovered_path:
            print(f"  Auto-discovered profile: {os.path.basename(discovered_path)}",
                  file=sys.stderr)
            args.profile = discovered_path
        elif count > 1:
            profiles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles")
            available = sorted(
                f for f in os.listdir(profiles_dir)
                if f.endswith(".json") and f != "base.json"
            )
            print("Multiple profiles found. Use --profile to specify:", file=sys.stderr)
            for p in available:
                print(f"  --profile profiles/{p}", file=sys.stderr)
            sys.exit(1)
        else:
            # No user profile — fall back to base.json if it exists
            base_fallback = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "profiles", "base.json"
            )
            if os.path.exists(base_fallback):
                print("  No user profile found. Using base defaults. "
                      "Run --calibrate to create your profile.", file=sys.stderr)
                args.profile = base_fallback

    # Load and apply voice profile if specified
    genre_word_target = None
    if args.profile:
        if not os.path.isfile(args.profile):
            print(f"Error: Profile not found: {args.profile}", file=sys.stderr)
            sys.exit(1)
        profile = load_profile(args.profile)
        genre_word_target = apply_profile(profile, genre=args.genre)
        profile_name = profile.get("profile", {}).get("name", os.path.basename(args.profile))
        if args.genre:
            genre_config = profile.get("genres", {}).get(args.genre)
            if not genre_config:
                available = list(profile.get("genres", {}).keys())
                print(f"Warning: Genre '{args.genre}' not found in profile. "
                      f"Available: {', '.join(available) if available else 'none'}. "
                      f"Using base thresholds.", file=sys.stderr)
    else:
        profile_name = None

    # Target priority: explicit --target > genre word_count_target > default 1200
    if args.target is not None:
        target = args.target
    elif genre_word_target is not None:
        target = genre_word_target
    else:
        target = 1200

    results = run_analysis(args.file, target)

    if results.get("empty"):
        print(f"\nFile has no body text (only headers or empty). Nothing to analyze.\n")
        sys.exit(0)

    if args.output_json:
        # Clean up non-serializable data for JSON output
        output = dict(results)
        if profile_name:
            output["profile"] = profile_name
        # Convert sentence tuples to dicts
        output["sentences"] = dict(results["sentences"])
        output["sentences"]["over_long"] = [
            {"sentence": s[:120], "words": w} for s, w in results["sentences"]["over_long"]
        ]
        output["sentences"]["over_rewrite"] = [
            {"sentence": s[:120], "words": w} for s, w in results["sentences"]["over_rewrite"]
        ]
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        flagged = results["flagged_sentences"]
        report = format_report(args.file, results, flagged)
        if profile_name:
            # Insert profile name into report header
            report = report.replace(
                "  VOICING REPORT:",
                f"  VOICING REPORT ({profile_name}):"
            )
        print(report)


if __name__ == "__main__":
    main()
