"""
Tests for genre support in writing_check.py.

Covers: genre threshold overrides, genre word count targets,
fallback behavior, default.json genre schema validation,
calibration genre output, and analysis with genre selection.
"""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import writing_check


# ---------------------------------------------------------------------------
# Expected genres — single source of truth for the test suite
# ---------------------------------------------------------------------------

EXPECTED_GENRES = [
    "academic_position",
    "tech_position",
    "edtech_position",
    "grant_application",
    "research_paper",
    "blog_essay",
    "social_media",
    "professional_correspondence",
]

REQUIRED_GENRE_KEYS = {"description", "word_count_target", "threshold_overrides", "genre_moves", "qualitative"}

VALID_QUALITATIVE_CATEGORIES = {"ideational", "interpersonal", "textual", "structural"}

VALID_THRESHOLD_KEYS = {
    "long_sentence_words", "rewrite_sentence_words", "long_sentence_max",
    "rewrite_sentence_max", "emdash_per_1000w", "emdash_insertion_words",
    "hedge_max", "self_aggrandizing_max", "topic_opener_max",
    "logical_connector_max", "narrative_padding_max", "product_description_max",
    "corporate_jargon_max", "wordcount_over_pct",
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def profile_with_genres():
    """Profile with base thresholds and two genre overrides."""
    return {
        "profile": {"name": "Genre Test User", "version": "1.0"},
        "patterns": {
            "hedge_words": ["\\bperhaps\\b"],
            "self_aggrandizing": [],
            "topic_sentence_starters": [],
            "logical_connectors": [],
            "narrative_padding": [],
            "corporate_jargon": [],
        },
        "thresholds": {
            "long_sentence_words": 45,
            "rewrite_sentence_words": 60,
            "hedge_max": 2,
            "logical_connector_max": 5,
            "wordcount_over_pct": 115,
        },
        "qualitative": [],
        "genres": {
            "tight_genre": {
                "description": "A genre with tight thresholds",
                "word_count_target": 300,
                "threshold_overrides": {
                    "hedge_max": 0,
                    "long_sentence_words": 30,
                },
                "genre_moves": ["hook", "point"],
                "qualitative": [
                    {
                        "id": "test_tight",
                        "category": "textual",
                        "name": "Tightness check",
                        "instruction": "Is it tight?",
                    }
                ],
            },
            "loose_genre": {
                "description": "A genre with loose thresholds",
                "word_count_target": 8000,
                "threshold_overrides": {
                    "hedge_max": 5,
                    "long_sentence_words": 60,
                    "rewrite_sentence_words": 80,
                    "logical_connector_max": 10,
                },
                "genre_moves": ["intro", "body", "conclusion"],
                "qualitative": [],
            },
            "minimal_genre": {
                "description": "A genre with no overrides",
                "word_count_target": 500,
                "threshold_overrides": {},
                "genre_moves": [],
                "qualitative": [],
            },
        },
    }


@pytest.fixture
def default_profile():
    """Load the actual default.json profile from disk."""
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "profiles", "default.json",
    )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def sample_draft(tmp_path):
    """A short draft for analysis tests."""
    content = """# Test Draft

This is a simple test draft. Perhaps this sentence hedges. Maybe too.
I built something. It works. The design was intentional.

This sentence is deliberately made to be fairly long so that it will
exceed tight genre thresholds but stay under loose ones for testing
the difference between genre configurations applied to the same text.
"""
    path = tmp_path / "genre_draft.md"
    path.write_text(content, encoding="utf-8")
    return str(path)


@pytest.fixture(autouse=True)
def reset_globals():
    """Reset writing_check globals to defaults before each test."""
    originals = {
        "HEDGE_WORDS": writing_check.HEDGE_WORDS[:],
        "SELF_AGGRANDIZING": writing_check.SELF_AGGRANDIZING[:],
        "TOPIC_SENTENCE_STARTERS": writing_check.TOPIC_SENTENCE_STARTERS[:],
        "LOGICAL_CONNECTORS": writing_check.LOGICAL_CONNECTORS[:],
        "NARRATIVE_PADDING": writing_check.NARRATIVE_PADDING[:],
        "CORPORATE_JARGON": writing_check.CORPORATE_JARGON[:],
        "THRESH_LONG_SENT": writing_check.THRESH_LONG_SENT,
        "THRESH_REWRITE_SENT": writing_check.THRESH_REWRITE_SENT,
        "THRESH_LONG_SENT_MAX": writing_check.THRESH_LONG_SENT_MAX,
        "THRESH_REWRITE_SENT_MAX": writing_check.THRESH_REWRITE_SENT_MAX,
        "THRESH_EMDASH_PER_1000": writing_check.THRESH_EMDASH_PER_1000,
        "THRESH_EMDASH_INSERT_WORDS": writing_check.THRESH_EMDASH_INSERT_WORDS,
        "THRESH_HEDGE_MAX": writing_check.THRESH_HEDGE_MAX,
        "THRESH_AGGRANDIZE_MAX": writing_check.THRESH_AGGRANDIZE_MAX,
        "THRESH_TOPIC_THIS_MAX": writing_check.THRESH_TOPIC_THIS_MAX,
        "THRESH_CONNECTOR_MAX": writing_check.THRESH_CONNECTOR_MAX,
        "THRESH_PADDING_MAX": writing_check.THRESH_PADDING_MAX,
        "THRESH_PRODUCT_MAX": writing_check.THRESH_PRODUCT_MAX,
        "THRESH_JARGON_MAX": writing_check.THRESH_JARGON_MAX,
        "THRESH_WORDCOUNT_OVER": writing_check.THRESH_WORDCOUNT_OVER,
    }
    yield
    for key, val in originals.items():
        setattr(writing_check, key, val)


# ---------------------------------------------------------------------------
# apply_profile genre parameter
# ---------------------------------------------------------------------------

class TestApplyProfileGenre:

    def test_no_genre_returns_none(self, profile_with_genres):
        result = writing_check.apply_profile(profile_with_genres)
        assert result is None

    def test_no_genre_uses_base_thresholds(self, profile_with_genres):
        writing_check.apply_profile(profile_with_genres)
        assert writing_check.THRESH_HEDGE_MAX == 2
        assert writing_check.THRESH_LONG_SENT == 45

    def test_genre_returns_word_count_target(self, profile_with_genres):
        result = writing_check.apply_profile(profile_with_genres, genre="tight_genre")
        assert result == 300

    def test_genre_returns_large_word_count_target(self, profile_with_genres):
        result = writing_check.apply_profile(profile_with_genres, genre="loose_genre")
        assert result == 8000

    def test_genre_overrides_specified_thresholds(self, profile_with_genres):
        writing_check.apply_profile(profile_with_genres, genre="tight_genre")
        assert writing_check.THRESH_HEDGE_MAX == 0
        assert writing_check.THRESH_LONG_SENT == 30

    def test_genre_preserves_non_overridden_thresholds(self, profile_with_genres):
        """Thresholds not in genre overrides should come from base profile."""
        writing_check.apply_profile(profile_with_genres, genre="tight_genre")
        # tight_genre only overrides hedge_max and long_sentence_words
        assert writing_check.THRESH_REWRITE_SENT == 60  # from base
        assert writing_check.THRESH_CONNECTOR_MAX == 5  # from base

    def test_loose_genre_overrides_multiple_thresholds(self, profile_with_genres):
        writing_check.apply_profile(profile_with_genres, genre="loose_genre")
        assert writing_check.THRESH_HEDGE_MAX == 5
        assert writing_check.THRESH_LONG_SENT == 60
        assert writing_check.THRESH_REWRITE_SENT == 80
        assert writing_check.THRESH_CONNECTOR_MAX == 10

    def test_empty_overrides_uses_base(self, profile_with_genres):
        """A genre with empty threshold_overrides should use all base thresholds."""
        writing_check.apply_profile(profile_with_genres, genre="minimal_genre")
        assert writing_check.THRESH_HEDGE_MAX == 2
        assert writing_check.THRESH_LONG_SENT == 45
        assert writing_check.THRESH_REWRITE_SENT == 60

    def test_empty_overrides_still_returns_word_target(self, profile_with_genres):
        result = writing_check.apply_profile(profile_with_genres, genre="minimal_genre")
        assert result == 500

    def test_nonexistent_genre_returns_none(self, profile_with_genres):
        result = writing_check.apply_profile(profile_with_genres, genre="nonexistent")
        assert result is None

    def test_nonexistent_genre_uses_base_thresholds(self, profile_with_genres):
        writing_check.apply_profile(profile_with_genres, genre="nonexistent")
        assert writing_check.THRESH_HEDGE_MAX == 2
        assert writing_check.THRESH_LONG_SENT == 45

    def test_profile_without_genres_key_ignores_genre(self):
        """Profiles from before genre support should work unchanged."""
        old_profile = {
            "thresholds": {"hedge_max": 3},
        }
        result = writing_check.apply_profile(old_profile, genre="anything")
        assert result is None
        assert writing_check.THRESH_HEDGE_MAX == 3

    def test_genre_none_same_as_no_genre(self, profile_with_genres):
        """Explicit genre=None should be identical to omitting genre."""
        writing_check.apply_profile(profile_with_genres, genre=None)
        hedge_none = writing_check.THRESH_HEDGE_MAX

        writing_check.apply_profile(profile_with_genres)
        hedge_omitted = writing_check.THRESH_HEDGE_MAX

        assert hedge_none == hedge_omitted == 2

    def test_genre_does_not_affect_patterns(self, profile_with_genres):
        """Genre overrides only affect thresholds, not pattern lists."""
        writing_check.apply_profile(profile_with_genres, genre="tight_genre")
        assert writing_check.HEDGE_WORDS == ["\\bperhaps\\b"]

    def test_different_genres_produce_different_thresholds(self, profile_with_genres):
        """Applying tight vs loose genre should produce different globals."""
        writing_check.apply_profile(profile_with_genres, genre="tight_genre")
        tight_hedge = writing_check.THRESH_HEDGE_MAX
        tight_long = writing_check.THRESH_LONG_SENT

        writing_check.apply_profile(profile_with_genres, genre="loose_genre")
        loose_hedge = writing_check.THRESH_HEDGE_MAX
        loose_long = writing_check.THRESH_LONG_SENT

        assert tight_hedge < loose_hedge
        assert tight_long < loose_long


# ---------------------------------------------------------------------------
# Genre-aware analysis
# ---------------------------------------------------------------------------

class TestGenreAwareAnalysis:

    def test_tight_genre_flags_more_sentences(self, profile_with_genres, sample_draft):
        """Tight genre (30-word threshold) should flag more long sentences."""
        writing_check.apply_profile(profile_with_genres)
        base_results = writing_check.run_analysis(sample_draft, target=1200)

        writing_check.apply_profile(profile_with_genres, genre="tight_genre")
        tight_results = writing_check.run_analysis(sample_draft, target=300)

        assert tight_results["sentences"]["over_long_count"] >= base_results["sentences"]["over_long_count"]

    def test_tight_genre_threshold_in_results(self, profile_with_genres, sample_draft):
        writing_check.apply_profile(profile_with_genres, genre="tight_genre")
        results = writing_check.run_analysis(sample_draft, target=300)
        assert results["sentences"]["long_threshold"] == 30

    def test_loose_genre_threshold_in_results(self, profile_with_genres, sample_draft):
        writing_check.apply_profile(profile_with_genres, genre="loose_genre")
        results = writing_check.run_analysis(sample_draft, target=8000)
        assert results["sentences"]["long_threshold"] == 60
        assert results["sentences"]["rewrite_threshold"] == 80


# ---------------------------------------------------------------------------
# default.json genre schema validation
# ---------------------------------------------------------------------------

class TestDefaultProfileGenres:

    def test_all_expected_genres_present(self, default_profile):
        genres = default_profile.get("genres", {})
        for genre_key in EXPECTED_GENRES:
            assert genre_key in genres, f"Missing genre: {genre_key}"

    def test_no_unexpected_genres(self, default_profile):
        genres = default_profile.get("genres", {})
        for genre_key in genres:
            assert genre_key in EXPECTED_GENRES, f"Unexpected genre: {genre_key}"

    def test_each_genre_has_required_keys(self, default_profile):
        for genre_key, config in default_profile["genres"].items():
            for key in REQUIRED_GENRE_KEYS:
                assert key in config, f"Genre '{genre_key}' missing key: {key}"

    def test_word_count_targets_are_positive_ints(self, default_profile):
        for genre_key, config in default_profile["genres"].items():
            target = config["word_count_target"]
            assert isinstance(target, int) and target > 0, (
                f"Genre '{genre_key}' word_count_target must be positive int, got {target}"
            )

    def test_threshold_overrides_are_valid_keys(self, default_profile):
        """Every key in threshold_overrides must be a recognized threshold name."""
        for genre_key, config in default_profile["genres"].items():
            for key in config["threshold_overrides"]:
                assert key in VALID_THRESHOLD_KEYS, (
                    f"Genre '{genre_key}' has unknown threshold override: {key}"
                )

    def test_threshold_overrides_are_numeric(self, default_profile):
        for genre_key, config in default_profile["genres"].items():
            for key, value in config["threshold_overrides"].items():
                assert isinstance(value, (int, float)), (
                    f"Genre '{genre_key}' threshold '{key}' must be numeric, got {type(value).__name__}"
                )

    def test_genre_moves_are_nonempty_strings(self, default_profile):
        for genre_key, config in default_profile["genres"].items():
            moves = config["genre_moves"]
            assert isinstance(moves, list), f"Genre '{genre_key}' genre_moves must be a list"
            assert len(moves) > 0, f"Genre '{genre_key}' should have at least one genre move"
            for move in moves:
                assert isinstance(move, str) and len(move) > 0, (
                    f"Genre '{genre_key}' has invalid genre move: {move!r}"
                )

    def test_qualitative_checks_have_valid_structure(self, default_profile):
        required_check_keys = {"id", "category", "name", "instruction"}
        for genre_key, config in default_profile["genres"].items():
            for check in config["qualitative"]:
                for key in required_check_keys:
                    assert key in check, (
                        f"Genre '{genre_key}' qualitative check missing key: {key}"
                    )
                assert check["category"] in VALID_QUALITATIVE_CATEGORIES, (
                    f"Genre '{genre_key}' check '{check['id']}' has invalid category: {check['category']}"
                )

    def test_qualitative_check_ids_unique_within_genre(self, default_profile):
        for genre_key, config in default_profile["genres"].items():
            ids = [c["id"] for c in config["qualitative"]]
            assert len(ids) == len(set(ids)), (
                f"Genre '{genre_key}' has duplicate qualitative check IDs: {ids}"
            )

    def test_qualitative_check_ids_unique_across_genres(self, default_profile):
        """No two genres should share a qualitative check ID (avoids confusion)."""
        all_ids = []
        for genre_key, config in default_profile["genres"].items():
            for check in config["qualitative"]:
                all_ids.append((genre_key, check["id"]))
        ids_only = [cid for _, cid in all_ids]
        duplicates = [cid for cid in ids_only if ids_only.count(cid) > 1]
        assert len(duplicates) == 0, f"Duplicate check IDs across genres: {set(duplicates)}"

    def test_descriptions_are_nonempty(self, default_profile):
        for genre_key, config in default_profile["genres"].items():
            assert len(config["description"]) > 20, (
                f"Genre '{genre_key}' description is too short to be useful"
            )

    def test_each_genre_loadable_with_apply_profile(self, default_profile):
        """Every genre in default.json should apply without error."""
        for genre_key in default_profile["genres"]:
            result = writing_check.apply_profile(default_profile, genre=genre_key)
            assert result is not None, f"Genre '{genre_key}' returned no word_count_target"
            assert isinstance(result, int), f"Genre '{genre_key}' word_count_target should be int"


# ---------------------------------------------------------------------------
# Genre register differentiation
# ---------------------------------------------------------------------------

class TestGenreRegisterDifferences:
    """Verify that genres produce meaningfully different threshold profiles."""

    def test_social_media_tighter_than_research_paper(self, default_profile):
        writing_check.apply_profile(default_profile, genre="social_media")
        social_hedge = writing_check.THRESH_HEDGE_MAX
        social_long = writing_check.THRESH_LONG_SENT

        writing_check.apply_profile(default_profile, genre="research_paper")
        research_hedge = writing_check.THRESH_HEDGE_MAX
        research_long = writing_check.THRESH_LONG_SENT

        assert social_hedge < research_hedge, "Social media should tolerate fewer hedges"
        assert social_long < research_long, "Social media should have shorter sentence threshold"

    def test_grant_allows_more_hedging_than_cover_letter(self, default_profile):
        writing_check.apply_profile(default_profile, genre="grant_application")
        grant_hedge = writing_check.THRESH_HEDGE_MAX

        writing_check.apply_profile(default_profile, genre="tech_position")
        tech_hedge = writing_check.THRESH_HEDGE_MAX

        assert grant_hedge > tech_hedge, "Grants should tolerate more hedging than tech cover letters"

    def test_research_paper_higher_word_target_than_social(self, default_profile):
        research_target = writing_check.apply_profile(default_profile, genre="research_paper")
        social_target = writing_check.apply_profile(default_profile, genre="social_media")
        assert research_target > social_target

    def test_each_genre_has_distinct_word_target(self, default_profile):
        """Not all genres should share the same word count target."""
        targets = set()
        for genre_key in default_profile["genres"]:
            t = writing_check.apply_profile(default_profile, genre=genre_key)
            targets.add(t)
        assert len(targets) >= 4, (
            f"Expected at least 4 distinct word targets across 8 genres, got {len(targets)}: {targets}"
        )


# ---------------------------------------------------------------------------
# Calibration includes genres key
# ---------------------------------------------------------------------------

class TestCalibrationGenreOutput:

    def test_calibrated_profile_has_genres_key(self, tmp_path):
        """Profiles generated by --calibrate should include an empty genres section."""
        samples = tmp_path / "samples"
        samples.mkdir()
        (samples / "s1.md").write_text(
            "I built this tool because the institution failed its students. "
            "It works well. The design reflects the critique. "
            "Every piece serves a purpose. I carried this into the next project. "
            "The conditions demanded it. I didn't plan to build software. "
            "The students needed something that worked. I made it. "
            "Four classes. Forty-nine students each. No teaching assistant. "
            "The automation wasn't a choice. It was survival. The numbers "
            "tell the story. Perhaps that sounds dramatic. It isn't.\n",
            encoding="utf-8",
        )
        output = tmp_path / "cal.json"
        writing_check.calibrate_from_samples(str(samples), str(output))

        profile = json.loads(output.read_text(encoding="utf-8"))
        assert "genres" in profile
        assert isinstance(profile["genres"], dict)

    def test_calibrated_genres_section_is_empty(self, tmp_path):
        """Calibration produces an empty genres dict — agent fills it during setup."""
        samples = tmp_path / "samples"
        samples.mkdir()
        (samples / "s1.md").write_text(
            "I built this tool because the institution failed its students. "
            "It works well. The design reflects the critique. "
            "Every piece serves a purpose. I carried this into the next project. "
            "The conditions demanded it. I didn't plan to build software. "
            "The students needed something that worked. I made it. "
            "Four classes. Forty-nine students each. No teaching assistant. "
            "The automation wasn't a choice. It was survival. The numbers "
            "tell the story. Perhaps that sounds dramatic. It isn't.\n",
            encoding="utf-8",
        )
        output = tmp_path / "cal.json"
        writing_check.calibrate_from_samples(str(samples), str(output))

        profile = json.loads(output.read_text(encoding="utf-8"))
        assert profile["genres"] == {}


# ---------------------------------------------------------------------------
# Backward compatibility with genre additions
# ---------------------------------------------------------------------------

class TestGenreBackwardCompatibility:

    def test_profile_without_genres_loads_and_applies(self):
        """Pre-genre profiles should still work without error."""
        old_profile = {
            "profile": {"name": "Old Profile", "version": "1.0"},
            "patterns": {"hedge_words": ["\\bperhaps\\b"]},
            "thresholds": {"hedge_max": 3},
            "qualitative": [],
        }
        result = writing_check.apply_profile(old_profile)
        assert result is None
        assert writing_check.THRESH_HEDGE_MAX == 3

    def test_profile_without_genres_ignores_genre_param(self):
        old_profile = {
            "thresholds": {"hedge_max": 3},
        }
        result = writing_check.apply_profile(old_profile, genre="research_paper")
        assert result is None
        assert writing_check.THRESH_HEDGE_MAX == 3

    def test_existing_tests_sample_profile_still_works(self):
        """The sample_profile fixture from test_voice_profiles.py has no genres key."""
        profile = {
            "patterns": {
                "hedge_words": ["\\bmaybe\\b"],
                "corporate_jargon": ["\\bsynergy\\b"],
            },
            "thresholds": {
                "long_sentence_words": 50,
                "hedge_max": 1,
                "wordcount_over_pct": 120,
            },
        }
        result = writing_check.apply_profile(profile)
        assert result is None
        assert writing_check.THRESH_LONG_SENT == 50
        assert writing_check.THRESH_HEDGE_MAX == 1
        assert writing_check.THRESH_WORDCOUNT_OVER == 1.2
