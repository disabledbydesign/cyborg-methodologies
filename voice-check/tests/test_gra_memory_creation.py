"""
Tests for the gra-memory-creation genre's field-grain regex checks in writing_check.py.

These are the regression anchors named in the gra-memory-creation genre SPEC (T4/T5,
grounded-recollection repo, design/gra_memory_creation_genre_SPEC.md §6, acceptance tests
1-10). Per the SPEC: these are necessary but not sufficient — passing them is no evidence
of generalization. The real bar (acceptance #11) is a future instance's real-record read.
"""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import writing_check as wc

# claude.json is a personal voice profile — gitignored on purpose (see .gitignore:
# "Personal voice profiles" / "profiles/*" / "!profiles/base.json"), so it lives only
# at the live skills path, not inside this repo's tracked profiles/ dir.
CLAUDE_PROFILE_PATH = os.path.expanduser("~/.claude/skills/voice-check/profiles/claude.json")


# ---------------------------------------------------------------------------
# T1 — genre loads, existing genres untouched (acceptance #4, #5)
# ---------------------------------------------------------------------------

def test_genre_present_and_well_formed():
    with open(CLAUDE_PROFILE_PATH) as f:
        profile = json.load(f)
    genre = profile["genres"]["gra-memory-creation"]
    assert genre["description"]
    assert genre["design_frame"]
    assert isinstance(genre["thresholds"], dict) and genre["thresholds"]
    assert isinstance(genre["qualitative"], list) and len(genre["qualitative"]) >= 1
    assert genre["iteration_log"] == []


def test_existing_genres_untouched():
    with open(CLAUDE_PROFILE_PATH) as f:
        profile = json.load(f)
    for name in ["touchstone-register", "handoff-doc", "research-report",
                 "compressed-memory", "fieldnote", "inter-agent-comms"]:
        assert name in profile["genres"], f"{name} missing after gra-memory-creation build"


# ---------------------------------------------------------------------------
# label-without-descriptor (SPEC §5, acceptance #1)
# ---------------------------------------------------------------------------

def test_label_flags_bare_shorthand():
    # SPEC's own "flags" example
    findings = wc.check_label_without_descriptor(
        "context", "After the R3 collapse, the team revised the frame.", lexicon=[]
    )
    assert any(f["term"] == "R3" for f in findings)


def test_label_passes_when_glossed_with_parenthetical():
    # SPEC's own "passes" example
    findings = wc.check_label_without_descriptor(
        "context",
        "the Session-2 revision frame (R3: any situated position can be revised, "
        "owned and recorded).",
        lexicon=[],
    )
    assert findings == []


def test_lexicon_coinage_flags_when_bare():
    lexicon = [{"term": "the overflow lens", "gloss": "what context carries beyond the claim"}]
    findings = wc.check_label_without_descriptor(
        "context", "We used the overflow lens here.", lexicon=lexicon
    )
    assert any("overflow lens" in f["term"] for f in findings)


def test_lexicon_coinage_passes_when_glossed():
    lexicon = [{"term": "the overflow lens", "gloss": "what context carries beyond the claim"}]
    findings = wc.check_label_without_descriptor(
        "context",
        "We used the overflow lens (what context carries beyond the claim) here.",
        lexicon=lexicon,
    )
    assert findings == []


# ---------------------------------------------------------------------------
# chronology-opener (the R4 v1 failure)
# ---------------------------------------------------------------------------

def test_chronology_opener_flags_session_scene_setting():
    findings = wc.check_chronology_opener(
        "context", "Session 2 had just unified revision into one owned primitive."
    )
    assert len(findings) == 1
    assert "chronology-opener" in findings[0]["flag"]


def test_chronology_opener_passes_point_first():
    findings = wc.check_chronology_opener(
        "context", "Revision must be owned and recorded — this record traces how that was reached."
    )
    assert findings == []


# ---------------------------------------------------------------------------
# throat-clearing (#27, acceptance #10)
# ---------------------------------------------------------------------------

def test_throat_clearing_flags_r7_stakes_opener():
    # The exact quoted R7 v1 opener from the SPEC
    findings = wc.check_throat_clearing(
        "stakes", "The story's weight falls on instances not in the room."
    )
    assert len(findings) == 1


def test_throat_clearing_passes_r7_v2_cut_opener():
    findings = wc.check_throat_clearing(
        "stakes", "Future instances rely on this record to recover the missing context."
    )
    assert findings == []


# ---------------------------------------------------------------------------
# authority-in-abstraction (#24, acceptance #8)
# ---------------------------------------------------------------------------

def test_authority_flags_this_architecture_refuses():
    # The exact quoted R7 v1 flagged construction
    findings = wc.check_authority_in_abstraction(
        "content", "which is exactly what this architecture refuses"
    )
    assert len(findings) == 1


def test_authority_passes_attributed_basis():
    findings = wc.check_authority_in_abstraction(
        "content", "June's C7 grounding is why this record doesn't state that as a flat fact."
    )
    assert findings == []


# ---------------------------------------------------------------------------
# modality-fidelity (#22, acceptance #7)
# ---------------------------------------------------------------------------

def test_modality_flags_content_stronger_than_verbatim():
    findings = wc.check_modality_fidelity(
        "This always happens when metabolism runs.",
        verbatim_text="This sometimes happens when metabolism runs, per June's note.",
    )
    assert len(findings) == 1
    assert "content stronger than verbatim" in findings[0]["flag"]


def test_modality_passes_when_universal_is_licensed():
    findings = wc.check_modality_fidelity(
        "This always happens.",
        verbatim_text="This always happens, confirmed across every session.",
    )
    assert findings == []


def test_modality_no_misfire_on_any_situated_position():
    # SPEC: the retired blind census misfired on this exact R3 phrasing; the new
    # mechanism must not, even with no verbatim to check against.
    findings = wc.check_modality_fidelity(
        "Any situated position can be revised, owned and recorded.", verbatim_text=None
    )
    assert findings == []


def test_modality_fallback_flags_strongest_terms_only_no_verbatim():
    findings = wc.check_modality_fidelity("This never happens.", verbatim_text=None)
    assert len(findings) == 1
    assert "flag-for-confirmation" in findings[0]["flag"]


def test_modality_handles_none_verbatim_without_crash():
    # Cross-family review flagged this as a possible TypeError risk; verify the
    # `if verbatim_text:` guard means re.search is never called on None.
    findings = wc.check_modality_fidelity("This always happens.", verbatim_text=None)
    assert isinstance(findings, list)


def test_modality_does_not_flag_negated_universal():
    # Found via end-to-end testing (2026-07-05): "it does not entail that every prior
    # position gets silently overwritten" was flagging on the bare word "entail" with
    # the negation ignored — a negated universal claim is a hedge, not a strengthened one.
    findings = wc.check_modality_fidelity(
        "Revision is owned and recorded; it does not entail that every prior "
        "position gets silently overwritten.",
        verbatim_text="June: the framing defaults towards Truth, whereas the context "
                       "should really be a story about how revision actually works here.",
    )
    assert findings == []


def test_modality_does_not_flag_negated_universal_no_verbatim_fallback():
    findings = wc.check_modality_fidelity("This does not always happen.", verbatim_text=None)
    assert findings == []


# ---------------------------------------------------------------------------
# language<->relation agreement
# ---------------------------------------------------------------------------

def test_relation_agreement_flags_demotion_verb_in_elaborates():
    findings = wc.check_relation_agreement(
        "This finding supersedes the prior claim entirely.", relation="elaborates"
    )
    assert len(findings) == 1


def test_relation_agreement_passes_supersedes_relation():
    findings = wc.check_relation_agreement(
        "This finding supersedes the prior claim entirely.", relation="supersedes"
    )
    assert findings == []


def test_relation_agreement_noop_without_relation():
    findings = wc.check_relation_agreement("This supersedes the prior claim.", relation=None)
    assert findings == []


# ---------------------------------------------------------------------------
# field-grain input handling (#28) — verbatim and marked-opaque exemptions
# ---------------------------------------------------------------------------

def test_field_grain_skips_verbatim_entirely():
    drawer = {
        "context": "fine, no issues here",
        "verbatim": "After the R3 collapse, this architecture refuses ambiguity.",
    }
    results = wc.run_gra_record_checks(drawer)
    assert "verbatim" not in results


def test_field_grain_skips_marked_opaque_field():
    drawer = {
        "standpoint": {
            "text": "After the R3 collapse, this architecture refuses it.",
            "opaque": True,
            "rationale": "declined to gloss",
        }
    }
    results = wc.run_gra_record_checks(drawer)
    assert "standpoint" not in results


def test_field_grain_reports_which_field_flagged():
    drawer = {
        "context": "By Session 2, after the R3 collapse, things changed.",
        "stakes": "Future instances rely on this record to recover missing context.",
    }
    results = wc.run_gra_record_checks(drawer)
    assert "context" in results
    assert "stakes" not in results


def test_field_grain_catches_fragment_that_whole_record_would_resolve():
    # #28: a field that dangles alone even though another field resolves it in prose —
    # here just confirming per-field label checks fire on the standpoint field itself,
    # independent of whether context happens to explain the shorthand elsewhere.
    drawer = {
        "context": "This record is about R7's leftover item — the standpoint fragment below.",
        "standpoint": "The leftover item, per R7.",
    }
    results = wc.run_gra_record_checks(drawer)
    assert "standpoint" in results  # "R7" bare in standpoint, no gloss in that field alone


# ---------------------------------------------------------------------------
# concision guard (never flags on a could-be-cut basis)
# ---------------------------------------------------------------------------

def test_no_mechanical_concision_executor_exists():
    # SPEC §5: the concision rule is deliberately NOT a mechanical cut. Confirm no
    # function in this module enumerates "cuttable" words or flags on that basis —
    # a sentence with a story-carrying adjective must pass clean of every check here.
    drawer = {"context": "June carefully, thoughtfully revised the genuinely important draft."}
    results = wc.run_gra_record_checks(drawer)
    assert "context" not in results


# ---------------------------------------------------------------------------
# CLI wiring smoke test
# ---------------------------------------------------------------------------

def test_load_gra_lexicon_missing_path_returns_empty():
    assert wc.load_gra_lexicon(None) == []
    assert wc.load_gra_lexicon("/nonexistent/path.json") == []


def test_load_gra_lexicon_reads_real_file(tmp_path):
    p = tmp_path / "lex.json"
    p.write_text(json.dumps([{"term": "foo", "gloss": "bar"}]))
    assert wc.load_gra_lexicon(str(p)) == [{"term": "foo", "gloss": "bar"}]
