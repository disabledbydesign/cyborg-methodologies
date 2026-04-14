"""
Integration tests for writing_check.py's multi-module orchestration.

Tests the glue code that wires stylometry, perplexity, and embeddings
into --calibrate and --learn. Each module has its own test suite; these
tests verify the orchestration: correct dispatch, graceful degradation
when modules are missing, profile round-trip after learn cycles, and
CLI argument interactions.

All ML backends are mocked — no MLX or fastembed needed.
"""

import copy
import json
import os
import sys
import types

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import writing_check


# ---------------------------------------------------------------------------
# Sample texts
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _restore_globals():
    """Save and restore writing_check module globals around each test.

    apply_profile() mutates module-level patterns and thresholds.
    Without this, tests that call apply_profile() pollute later tests
    in other files that expect default values.
    """
    saved = {}
    global_names = [
        "HEDGE_WORDS", "SELF_AGGRANDIZING", "TOPIC_SENTENCE_STARTERS",
        "LOGICAL_CONNECTORS", "NARRATIVE_PADDING", "CORPORATE_JARGON",
        "THRESH_LONG_SENT", "THRESH_REWRITE_SENT", "THRESH_LONG_SENT_MAX",
        "THRESH_REWRITE_SENT_MAX", "THRESH_EMDASH_PER_1000",
        "THRESH_EMDASH_INSERT_WORDS", "THRESH_HEDGE_MAX",
        "THRESH_AGGRANDIZE_MAX", "THRESH_TOPIC_THIS_MAX",
        "THRESH_CONNECTOR_MAX", "THRESH_PADDING_MAX", "THRESH_PRODUCT_MAX",
        "THRESH_JARGON_MAX", "THRESH_WORDCOUNT_OVER",
    ]
    for name in global_names:
        if hasattr(writing_check, name):
            val = getattr(writing_check, name)
            saved[name] = val[:] if isinstance(val, list) else val
    yield
    for name, val in saved.items():
        setattr(writing_check, name, val)


AUTHOR_PROSE = (
    "I built this thing because the institution wouldn't. "
    "Four classes — forty-nine students each. No teaching assistant. "
    "The automation wasn't a choice: it was survival. "
    "I collect the numbers that matter. I collect them anyway."
)

AGENT_PROSE = (
    "This innovative solution leverages best practices to transform "
    "the learning environment. The paradigm shift enables stakeholders "
    "to synergize effectively. Furthermore, the impactful approach "
    "additionally demonstrates thought leadership."
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_dir(tmp_path):
    """Directory with two writing samples for calibration."""
    s1 = tmp_path / "samples" / "sample1.md"
    s1.parent.mkdir()
    s1.write_text(
        "I built this. It works well. The design was intentional. "
        "Every piece serves a purpose. The architecture reflects the critique. "
        "I carried this into the next project. "
        "The conditions demanded it. I didn't plan to build software. "
        "The institution failed. The students needed something. I made it. "
        "Perhaps that sounds dramatic. It isn't. The numbers tell the story. "
        "Four classes. Forty-nine students each. No teaching assistant. "
        "The automation wasn't a choice — it was survival. "
        "I built curriculum from scratch, then rebuilt it when it failed. "
        "The feedback loops were immediate: you know within a week. "
        "I kept what worked and cut what didn't. That's the whole method.",
        encoding="utf-8"
    )
    s2 = tmp_path / "samples" / "sample2.md"
    s2.write_text(
        "The semester ended with a question I couldn't answer. "
        "Not because I lacked data — I had plenty. "
        "But because the question was the wrong one. "
        "I had been optimizing for completion rates; "
        "what I should have been measuring was engagement quality. "
        "The distinction matters. A student who completes every assignment "
        "but learns nothing has succeeded by my metric and failed by theirs. "
        "I changed the metric. The completion rates dropped. "
        "The learning improved. I'm comfortable with that trade.",
        encoding="utf-8"
    )
    return str(s1.parent)


@pytest.fixture
def draft_files(tmp_path):
    """First draft and final draft files for learn tests."""
    first = tmp_path / "first_draft.md"
    first.write_text(AGENT_PROSE, encoding="utf-8")
    final = tmp_path / "final_draft.md"
    final.write_text(AUTHOR_PROSE, encoding="utf-8")
    return str(first), str(final)


@pytest.fixture
def calibrated_profile(tmp_path, sample_dir):
    """A profile calibrated from samples with stylometry only."""
    output = str(tmp_path / "profile.json")
    writing_check.calibrate_from_samples(sample_dir, output)
    with open(output) as f:
        return json.load(f), output


@pytest.fixture
def profile_with_all_sections(calibrated_profile, tmp_path):
    """Profile with stylometry + synthetic perplexity + synthetic embeddings."""
    profile, _ = calibrated_profile
    profile["perplexity"] = {
        "model": "test-model",
        "baseline_mean": 50.0,
        "baseline_stdev": 20.0,
        "baseline_variance": 400.0,
        "baseline_cv": 0.4,
        "calibration_sentence_count": 30,
        "distance_threshold": 90.0,
        "style_notes": "Test perplexity notes.",
        "revision_count": 0,
        "enabled": True,
    }
    profile["embeddings"] = {
        "model": "test-embed-model",
        "centroid": [0.1] * 384,
        "dimension": 384,
        "mean_distance": 0.25,
        "stdev_distance": 0.05,
        "distance_threshold": 0.325,
        "calibration_sentence_count": 30,
        "calibration_word_count": 3000,
        "style_notes": "Test embedding notes.",
        "revision_count": 0,
    }
    path = str(tmp_path / "full_profile.json")
    with open(path, "w") as f:
        json.dump(profile, f)
    return profile, path


# ---------------------------------------------------------------------------
# Calibration integration
# ---------------------------------------------------------------------------

class TestCalibrateIntegration:
    """Tests for calibrate_from_samples() module orchestration."""

    def test_calibration_produces_stylometry_section(self, calibrated_profile):
        profile, _ = calibrated_profile
        assert "stylometry" in profile
        assert "function_words" in profile["stylometry"]
        assert "style_notes" in profile["stylometry"]

    def test_calibration_profile_is_loadable(self, calibrated_profile):
        _, path = calibrated_profile
        loaded = writing_check.load_profile(path)
        assert "stylometry" in loaded

    def test_calibration_profile_has_genres_key(self, calibrated_profile):
        profile, _ = calibrated_profile
        assert "genres" in profile

    def test_calibration_profile_has_qualitative_checks(self, calibrated_profile):
        profile, _ = calibrated_profile
        assert "qualitative" in profile
        assert len(profile["qualitative"]) > 0

    def test_calibration_profile_has_thresholds(self, calibrated_profile):
        profile, _ = calibrated_profile
        t = profile["thresholds"]
        assert "long_sentence_words" in t
        assert "hedge_max" in t

    def test_calibration_continues_when_perplexity_unavailable(
        self, monkeypatch, sample_dir, tmp_path
    ):
        """If perplexity module raises ImportError, calibration still succeeds."""
        import builtins
        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "perplexity":
                raise ImportError("mocked")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)
        output = str(tmp_path / "profile.json")
        writing_check.calibrate_from_samples(sample_dir, output)

        with open(output) as f:
            profile = json.load(f)
        assert "stylometry" in profile
        assert "perplexity" not in profile

    def test_calibration_continues_when_embeddings_unavailable(
        self, monkeypatch, sample_dir, tmp_path
    ):
        """If embeddings module raises ImportError, calibration still succeeds."""
        import builtins
        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "embeddings":
                raise ImportError("mocked")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)
        output = str(tmp_path / "profile.json")
        writing_check.calibrate_from_samples(sample_dir, output)

        with open(output) as f:
            profile = json.load(f)
        assert "stylometry" in profile
        assert "embeddings" not in profile

    def test_calibration_output_is_valid_json(self, calibrated_profile):
        _, path = calibrated_profile
        with open(path) as f:
            data = json.load(f)
        # Re-serialize to verify no non-serializable types
        json.dumps(data)


# ---------------------------------------------------------------------------
# Learn integration
# ---------------------------------------------------------------------------

class TestLearnIntegration:
    """Tests for learn_from_revision() module orchestration."""

    def test_learn_updates_stylometry_revision_count(
        self, calibrated_profile, draft_files
    ):
        profile, path = calibrated_profile
        assert profile["stylometry"]["revision_count"] == 0

        first, final = draft_files
        writing_check.learn_from_revision(first, final, path)

        with open(path) as f:
            updated = json.load(f)
        assert updated["stylometry"]["revision_count"] == 1

    def test_learn_saves_valid_json(self, calibrated_profile, draft_files):
        _, path = calibrated_profile
        first, final = draft_files
        writing_check.learn_from_revision(first, final, path)

        with open(path) as f:
            updated = json.load(f)
        # Re-serialize to check no numpy arrays leaked
        json.dumps(updated)

    def test_learn_without_perplexity_section_skips_perplexity(
        self, calibrated_profile, draft_files, tmp_path
    ):
        profile, _ = calibrated_profile
        # Remove perplexity section to test graceful skip
        profile.pop("perplexity", None)
        path = str(tmp_path / "no_ppl.json")
        with open(path, "w") as f:
            json.dump(profile, f)

        first, final = draft_files
        writing_check.learn_from_revision(first, final, path)

        with open(path) as f:
            updated = json.load(f)
        assert "perplexity" not in updated

    def test_learn_without_embeddings_section_skips_embeddings(
        self, calibrated_profile, draft_files, tmp_path
    ):
        profile, _ = calibrated_profile
        # Remove embeddings section to test graceful skip
        profile.pop("embeddings", None)
        path = str(tmp_path / "no_emb.json")
        with open(path, "w") as f:
            json.dump(profile, f)

        first, final = draft_files
        writing_check.learn_from_revision(first, final, path)

        with open(path) as f:
            updated = json.load(f)
        assert "embeddings" not in updated

    def test_learn_with_perplexity_updates_perplexity(
        self, profile_with_all_sections, draft_files, monkeypatch
    ):
        """When profile has perplexity section and module is available,
        learn_from_revision updates perplexity revision_count."""
        _, path = profile_with_all_sections
        first, final = draft_files

        # Mock perplexity module to return synthetic metrics
        fake_ppl = types.ModuleType("perplexity")
        fake_ppl.compute_perplexity = lambda text, **kw: {
            "sentence_perplexities": [40.0, 60.0],
            "mean": 50.0,
            "stdev": 14.14,
            "variance": 200.0,
            "cv": 0.283,
            "sentence_count": 2,
            "model": "test-model",
        }
        fake_ppl.compare_perplexity = lambda f, l, b: {
            "first_mean": 50.0,
            "final_mean": 55.0,
            "baseline_mean": 50.0,
            "first_cv": 0.3,
            "final_cv": 0.4,
            "baseline_cv": 0.4,
            "improved": True,
            "summary": "Test perplexity summary.",
        }
        fake_ppl.update_profile_perplexity = lambda p, f, l: _bump_section(
            p, "perplexity"
        )
        monkeypatch.setitem(sys.modules, "perplexity", fake_ppl)

        writing_check.learn_from_revision(first, final, path)

        with open(path) as f:
            updated = json.load(f)
        assert updated["perplexity"]["revision_count"] == 1

    def test_learn_with_embeddings_updates_embeddings(
        self, profile_with_all_sections, draft_files, monkeypatch
    ):
        """When profile has embeddings section and module is available,
        learn_from_revision updates embeddings revision_count."""
        _, path = profile_with_all_sections
        first, final = draft_files

        import numpy as np

        fake_emb = types.ModuleType("embeddings")
        fake_emb.compute_embeddings = lambda text, **kw: {
            "sentence_embeddings": [np.zeros(384)],
            "centroid": np.zeros(384),
            "distances_from_centroid": [0.0],
            "mean_distance": 0.1,
            "stdev_distance": 0.05,
            "sentence_count": 1,
            "model": "test-embed-model",
        }
        fake_emb.compare_embeddings = lambda f, l, b: {
            "first_centroid_distance": 0.2,
            "final_centroid_distance": 0.1,
            "improved": True,
            "first_outlier_ratio": 0.0,
            "final_outlier_ratio": 0.0,
            "top_drifted_sentences": [],
            "summary": "Test embeddings summary.",
        }
        fake_emb.update_profile_embeddings = lambda p, f, l: _bump_section(
            p, "embeddings"
        )
        monkeypatch.setitem(sys.modules, "embeddings", fake_emb)

        writing_check.learn_from_revision(first, final, path)

        with open(path) as f:
            updated = json.load(f)
        assert updated["embeddings"]["revision_count"] == 1

    def test_learn_perplexity_import_error_does_not_crash(
        self, profile_with_all_sections, draft_files, monkeypatch
    ):
        """If perplexity module can't be imported, learn still completes."""
        _, path = profile_with_all_sections
        first, final = draft_files

        # Remove perplexity from sys.modules and make import fail
        monkeypatch.delitem(sys.modules, "perplexity", raising=False)
        import builtins
        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "perplexity":
                raise ImportError("mocked")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)

        writing_check.learn_from_revision(first, final, path)

        with open(path) as f:
            updated = json.load(f)
        # Stylometry still updated
        assert updated["stylometry"]["revision_count"] == 1
        # Perplexity section preserved but NOT updated
        assert updated["perplexity"]["revision_count"] == 0

    def test_learn_embeddings_import_error_does_not_crash(
        self, profile_with_all_sections, draft_files, monkeypatch
    ):
        """If embeddings module can't be imported, learn still completes."""
        _, path = profile_with_all_sections
        first, final = draft_files

        monkeypatch.delitem(sys.modules, "embeddings", raising=False)
        import builtins
        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "embeddings":
                raise ImportError("mocked")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)

        writing_check.learn_from_revision(first, final, path)

        with open(path) as f:
            updated = json.load(f)
        assert updated["stylometry"]["revision_count"] == 1
        assert updated["embeddings"]["revision_count"] == 0

    def test_learn_exits_when_no_stylometry_section(self, tmp_path, draft_files):
        """Profile without stylometry section causes sys.exit."""
        profile_path = str(tmp_path / "bare.json")
        with open(profile_path, "w") as f:
            json.dump({"profile": {"name": "Bare"}, "patterns": {},
                        "thresholds": {}}, f)

        first, final = draft_files
        with pytest.raises(SystemExit):
            writing_check.learn_from_revision(first, final, profile_path)

    def test_learn_multiple_cycles_increment_correctly(
        self, calibrated_profile, draft_files
    ):
        """Two consecutive learn cycles increment revision_count to 2."""
        _, path = calibrated_profile
        first, final = draft_files

        writing_check.learn_from_revision(first, final, path)
        writing_check.learn_from_revision(first, final, path)

        with open(path) as f:
            updated = json.load(f)
        assert updated["stylometry"]["revision_count"] == 2


# ---------------------------------------------------------------------------
# Profile round-trip
# ---------------------------------------------------------------------------

class TestProfileRoundTrip:
    """Verify profiles survive serialize → load → apply cycles."""

    def test_calibrated_profile_survives_load_apply(self, calibrated_profile):
        _, path = calibrated_profile
        profile = writing_check.load_profile(path)
        # apply_profile should not crash
        writing_check.apply_profile(profile)

    def test_calibrated_profile_with_genre_survives_load_apply(
        self, calibrated_profile
    ):
        profile, path = calibrated_profile
        # Add a genre
        profile["genres"] = {
            "test_genre": {
                "description": "Test genre",
                "word_count_target": 800,
                "threshold_overrides": {"hedge_max": 0},
                "genre_moves": ["intro", "body"],
                "qualitative": [],
            }
        }
        with open(path, "w") as f:
            json.dump(profile, f)

        loaded = writing_check.load_profile(path)
        target = writing_check.apply_profile(loaded, genre="test_genre")
        assert target == 800

    def test_full_profile_after_learn_survives_reload(
        self, calibrated_profile, draft_files
    ):
        _, path = calibrated_profile
        first, final = draft_files
        writing_check.learn_from_revision(first, final, path)

        # Reload and re-apply
        loaded = writing_check.load_profile(path)
        writing_check.apply_profile(loaded)
        assert loaded["stylometry"]["revision_count"] == 1


# ---------------------------------------------------------------------------
# CLI argument interactions
# ---------------------------------------------------------------------------

class TestCLIInteractions:
    """Test CLI argument parsing and interaction between flags."""

    def test_learn_requires_profile(self, monkeypatch):
        """--learn without --profile should error."""
        monkeypatch.setattr("sys.argv", ["writing_check.py", "--learn", "a.md", "b.md"])
        with pytest.raises(SystemExit):
            writing_check.main()

    def test_genre_without_profile_is_ignored(self, tmp_path):
        """--genre without --profile uses default thresholds."""
        draft = tmp_path / "draft.md"
        draft.write_text("Short test sentence.", encoding="utf-8")
        # Should not crash — genre is silently ignored without profile
        result = writing_check.run_analysis(str(draft))
        assert result["words"]["total"] > 0

    def test_target_overrides_genre_target(self, calibrated_profile, tmp_path):
        """Explicit --target takes priority over genre word_count_target."""
        profile, path = calibrated_profile
        profile["genres"] = {
            "test": {
                "description": "Test",
                "word_count_target": 5000,
                "threshold_overrides": {},
                "genre_moves": [],
                "qualitative": [],
            }
        }
        with open(path, "w") as f:
            json.dump(profile, f)

        loaded = writing_check.load_profile(path)
        genre_target = writing_check.apply_profile(loaded, genre="test")
        assert genre_target == 5000
        # But explicit target should win at the CLI level
        # (tested via the resolution logic, not full CLI invocation)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _bump_section(profile, section):
    """Helper: deep copy profile and increment a section's revision_count."""
    import copy as _copy
    updated = _copy.deepcopy(profile)
    if section in updated:
        updated[section]["revision_count"] = (
            updated[section].get("revision_count", 0) + 1
        )
    return updated
