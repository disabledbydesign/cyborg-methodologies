#!/usr/bin/env python3
"""
check_pdf_textlayer.py — verification gate for submitted PDFs.

Reads the *rendered artifact's text layer* (what a parser actually receives),
not the HTML/Markdown source. Nothing else in this pipeline does that.

Guards the failure named in PIPELINE.md Step 4.4: the document arrives
illegible or with blank fields, not "the machine rejects you."

Usage:
    python3 check_pdf_textlayer.py "Some App/Bloch CL.pdf" [more.pdf ...]
    python3 check_pdf_textlayer.py --show "Some App/Bloch Resume.pdf"

Exit 0 = clean, 1 = at least one BLOCK-level finding.
Requires: pdftotext (poppler). Already installed.
"""
import re, subprocess, sys, os

GREENHOUSE_PARSE_CEILING = 2.5 * 1024 * 1024   # documented; larger uploads OK but unparsed
MIN_CHARS_PER_PAGE = 200                        # below this, suspect image-only

# Header words a parser looks for when populating structured profile fields.
HEADER_WORDS = ["EDUCATION", "EXPERIENCE", "EMPLOYMENT", "SKILLS", "PUBLICATIONS",
                "SUMMARY", "COMPETENCIES", "TEACHING", "AWARDS", "CERTIFICATIONS"]


def pdftotext(path, layout=False):
    cmd = ["pdftotext"] + (["-layout"] if layout else []) + [path, "-"]
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def n_pages(path):
    out = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else 1


def shattered_lines(text):
    """Lines mangled by CSS letter-spacing: glyphs emitted as separate tokens."""
    hits = []
    for line in text.split("\n"):
        toks = line.split()
        if len(toks) < 4:
            continue
        singles = sum(1 for t in toks if len(t.strip("·&,.-")) == 1 and t.isascii())
        if singles / len(toks) >= 0.5:
            hits.append(line.strip())
    return hits


def split_words(text):
    """Word-internal breaks: 'EDUC ATION', 'SCHOL AR'. Catches milder tracking damage."""
    hits = []
    for w in HEADER_WORDS:
        for i in range(2, len(w) - 1):
            frag = w[:i] + " " + w[i:]
            if frag in text.upper():
                hits.append(frag)
    return sorted(set(hits))


def check(path, show=False):
    findings = []
    size = os.path.getsize(path)
    raw = pdftotext(path)
    pages = n_pages(path)

    if size > GREENHOUSE_PARSE_CEILING:
        findings.append(("BLOCK", f"{size/1024/1024:.1f} MB exceeds the 2.5 MB Greenhouse "
                                  f"parse ceiling. Uploads cleanly, parses to nothing."))
    prod = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"Producer:\s+(.+)", prod)
    producer = m.group(1).strip() if m else "?"
    if "Quartz" in producer:
        findings.append(("BLOCK", f"Producer is '{producer}' — this PDF was re-saved through "
                                  f"macOS Preview / the system print dialog, which flattened the "
                                  f"text to an image. Re-export with Chrome's own 'Save as PDF' "
                                  f"destination (Producer should read 'Skia/PDF')."))

    if len(raw.strip()) / max(pages, 1) < MIN_CHARS_PER_PAGE:
        findings.append(("BLOCK", f"Only {len(raw.strip())} chars across {pages} page(s) — "
                                  f"likely image-only. Recruiter gets blank fields."))

    sh = shattered_lines(raw)
    if sh:
        findings.append(("BLOCK", "Letter-spacing shatters these lines in the text layer "
                                  "(fix: lower CSS letter-spacing to <= 0.06em):"))
        findings += [("  ", "  " + s) for s in sh[:8]]

    sw = split_words(raw)
    if sw:
        findings.append(("BLOCK", f"Section-header words broken mid-token: {', '.join(sw)}. "
                                  f"A parser will not match these to a profile field."))

    up = raw.upper()
    missing = [w for w in ("EDUCATION", "EXPERIENCE") if w not in up]
    if missing and "resume" in path.lower():
        findings.append(("WARN", f"No intact '{'/'.join(missing)}' header found."))

    if "linkedin.com/in/" not in raw.lower() and re.search(r"\bl-june-bloch\b", raw):
        findings.append(("WARN", "LinkedIn appears as a bare handle with no URL — "
                                 "parsers extract the field from the full URL."))

    print(f"\n=== {path}  ({size/1024:.0f} KB, {pages}p) ===")
    if not findings:
        print("  clean")
    for level, msg in findings:
        print(f"  [{level}] {msg}" if level.strip() else msg)

    if show:
        print("\n  --- first 30 lines, parser reading order ---")
        for line in raw.split("\n")[:30]:
            print("  | " + line)

    return any(l == "BLOCK" for l, _ in findings)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--show"]
    show = "--show" in sys.argv
    if not args:
        print(__doc__); sys.exit(2)
    bad = [check(p, show) for p in args if os.path.exists(p)]
    sys.exit(1 if any(bad) else 0)
