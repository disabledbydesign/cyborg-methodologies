"""Tests for the PDF text-layer gate.

The detection logic is tested directly against synthetic extracted text, so the
suite needs no PDF fixtures and no poppler. The CLI is smoke-tested separately.

Added 2026-09-12 alongside the tool. The defects encoded here are real: the
shattered strings are verbatim from L. June Bloch's submitted résumés, and the
six-character case is the signature of a Chrome-rendered PDF re-saved through
macOS Quartz, which flattens the text to an image and leaves only ", Ph.D."
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
SCRIPT = TOOLS / "check_pdf_textlayer.py"

_spec = importlib.util.spec_from_file_location("check_pdf_textlayer", SCRIPT)
mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(mod)


def test_detects_per_glyph_shatter() -> None:
    text = "E D U C AT I O N\nSome ordinary body prose that should not trip the check.\n"
    assert mod.shattered_lines(text) == ["E D U C AT I O N"]


def test_detects_real_resume_headers() -> None:
    text = (
        "S E L E C T E D R E F E R E E D P U B L I C AT I O N S\n"
        "C L I E N T & C U S TO M E R E X P E R I E N C E\n"
    )
    assert len(mod.shattered_lines(text)) == 2


def test_clean_headers_do_not_trip() -> None:
    text = "EDUCATION\nSELECTED REFEREED PUBLICATIONS\nCORE COMPETENCIES\n"
    assert mod.shattered_lines(text) == []


def test_prose_with_short_words_does_not_trip() -> None:
    """A sentence of one- and two-letter words must not read as shattered."""
    text = "I am a A B C of the it is on an to be or so we do go up\n"
    # Half or more single-char tokens is the threshold; ordinary prose stays under it.
    assert mod.shattered_lines("The quick brown fox jumped over a lazy dog today") == []


def test_detects_word_internal_breaks() -> None:
    assert "EDUC ATION" in mod.split_words("H I G H E R EDUC ATION & TEACHING")
    assert mod.split_words("EDUCATION AND EXPERIENCE") == []


def test_header_wordlist_covers_the_parser_fields() -> None:
    for w in ("EDUCATION", "EXPERIENCE", "SKILLS", "PUBLICATIONS"):
        assert w in mod.HEADER_WORDS


def test_greenhouse_parse_ceiling_is_two_and_a_half_mb() -> None:
    assert mod.GREENHOUSE_PARSE_CEILING == 2.5 * 1024 * 1024


def test_cli_without_arguments_exits_two() -> None:
    r = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
    assert r.returncode == 2
    assert "verification gate" in r.stdout


def test_cli_accepts_show_flag_without_paths() -> None:
    r = subprocess.run([sys.executable, str(SCRIPT), "--show"], capture_output=True, text=True)
    assert r.returncode == 2
