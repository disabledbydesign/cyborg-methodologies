# CGT Analysis Skill — Buildable Spec

*Status: IN PROGRESS — workshopping step by step from DESIGN_PLAN.md*
*Started: 2026-04-07*

---

## 2a. Data Intake & Project Initialization

### Data Intake

The skill accepts qualitative data in any text-based format. It does not prescribe or assume a specific data source — the researcher brings whatever data they're analyzing.

**Input methods** (in order of expected frequency):
1. **File path** — single file: `/cgt analyze path/to/transcript.txt`
2. **Directory** — all files in a directory: `/cgt analyze path/to/interviews/`
3. **Inline text** — pasted directly into the conversation for quick coding

**Supported formats**: Any text-readable file — `.txt`, `.md`, `.pdf`, `.docx`, etc. The skill reads the content; it doesn't care about the container. For directories, the skill processes all readable files and presents the researcher with what it found before proceeding.

**No format transformation**: The skill works with the data as-is. It does not require the researcher to reformat, pre-process, or structure their data before analysis. Chunking (see 3b) happens internally.

### Project Initialization

Each CGT project is a directory with a standard structure. Projects are isolated — separate codebook, memos, categories, and orientation context.

**Directory structure**:
```
cgt_projects/
├── ai_welfare/
│   ├── PROJECT.md          # orientation context, sensitizing concepts, project metadata
│   ├── codebook.md         # evolving codebook (the few-shot exemplar source)
│   ├── memos/              # analytical memos
│   ├── sessions/           # per-session coding logs and outputs
│   └── data/               # optional — data can live anywhere, project just references it
├── autograder_sessions/
│   ├── PROJECT.md
│   ├── codebook.md
│   ├── memos/
│   ├── sessions/
│   └── data/
```

**Project init creates**:
- The project directory and subdirectories
- A `PROJECT.md` seeded from the orientation dialogue
- An empty `codebook.md` with initial structure
- Empty `memos/` and `sessions/` directories

**`PROJECT.md` contents** (skeleton — refined through use with real projects):
- Project name and description
- What data is being analyzed and why
- Researcher's disciplinary position and commitments (as surfaced through dialogue)
- Sensitizing concepts the researcher is bringing
- Analytical orientation notes (evolves over the life of the project)
- Rigor level default for this project
- Pointers to data sources (file paths, not copies)

**Orientation dialogue**: At project init, the skill asks open-ended questions to surface the researcher's starting position — what they're studying, why, what they expect to find, what disciplinary lenses they're working from. This is captured in `PROJECT.md` and referenced during coding. The dialogue format and specific questions will be refined through testing with real projects. The goal is usefulness, not performative reflexivity.

**Cross-project synthesis**: Handled separately in Phase 6b (master library). Individual projects don't need to know about each other.
