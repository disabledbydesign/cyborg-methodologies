"""Shared helpers for the Kit tools.

The only subtle thing in here is `normalize()`. Everything downstream depends on it:
verify.py proves a fact is real by checking that its quote appears verbatim in the
extracted source text, and "verbatim" has to survive the round trip through Google Docs
smart quotes, PDF ligatures, and OCR whitespace. Normalization is deliberately
conservative -- it folds typography, never words. Folding words would let a paraphrase
pass as a quote, which is the one thing this check exists to prevent.
"""

import json
import os
import re
import unicodedata
from pathlib import Path

BASE = Path("/Users/june/Documents/Filing/Consulting")
KIT = Path(__file__).resolve().parent.parent

# These three default to exactly today's behavior (co-located with KIT) so the
# ORIGINAL Kit folder needs zero changes and zero env vars to keep working.
# They only need to be set when running these tools from a split-out location
# like knowledge-layer/, where the raw sources and working-directory material
# were deliberately left behind in the original Kit folder.
SOURCES_HOME = Path(os.environ["RUSTIN_KIT_SOURCES_DIR"]) if os.environ.get("RUSTIN_KIT_SOURCES_DIR") else KIT / "sources"
WORKDIR_HOME = Path(os.environ["RUSTIN_KIT_WORKDIR"]) if os.environ.get("RUSTIN_KIT_WORKDIR") else KIT
# GRANTS_HOME's plain co-located default (KIT.parent) is wrong one level too shallow --
# funders.json etc. live in KIT.parent/grants-research, not KIT.parent itself, because
# grants-research is its own split-out sibling folder, not something left behind next to
# KIT the way sources/ and the workdir material were. No env-loading mechanism exists in
# this repo for RUSTIN_GRANTS_HOME (checked: no .envrc/Makefile/wrapper sources it, and
# the .env files under Rustin Institute/ are for the unrelated receipts app's own secrets
# store, not read by anything here), so nobody has ever set it. Rather than require an env
# var nobody sets, detect the real sibling folder and fall back to the old behavior only if
# it's somehow not there.
GRANTS_HOME = (
    Path(os.environ["RUSTIN_GRANTS_HOME"]) if os.environ.get("RUSTIN_GRANTS_HOME")
    else KIT.parent / "grants-research" if (KIT.parent / "grants-research").exists()
    else KIT.parent
)

TEXT = SOURCES_HOME / "text"

# Typographic variants that mean the same character. Extraction tools disagree about
# these constantly; a quote copied from a .md file will not otherwise match the same
# sentence pulled out of a PDF.
_CHAR_MAP = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    "′": "'", "″": '"',
    "‐": "-", "‑": "-", "‒": "-", "–": "-",
    "—": "-", "―": "-", "−": "-",
    " ": " ", " ": " ", " ": " ", " ": " ", " ": " ",
    "​": "", "‌": "", "‍": "", "﻿": "",
    "…": "...",
    "ﬁ": "fi", "ﬂ": "fl",
    "­": "",  # soft hyphen, inserted by some PDF extractors mid-word
}


def normalize(s: str) -> str:
    """Fold typography and whitespace so a quote can be matched across extractors.

    Case is preserved -- a claim that changes case changes meaning often enough
    (proper nouns, acronyms) that folding it would hide real drift.
    """
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", s)
    for a, b in _CHAR_MAP.items():
        s = s.replace(a, b)
    # Collapse all whitespace runs, including newlines: line wrapping is an artifact
    # of the extractor, not of the document.
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def load_sources() -> list[dict]:
    p = SOURCES_HOME / "sources.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    return data["sources"]


def load_facts() -> list[dict]:
    p = KIT / "facts.json"
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return data.get("facts", [])


def source_text(source_id: str) -> str | None:
    p = TEXT / f"{source_id}.txt"
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8", errors="replace")


def resolve(path_rel: str) -> Path:
    return BASE / path_rel
