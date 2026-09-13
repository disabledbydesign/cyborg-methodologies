# Hakope's Question — Tool Concept

**Status:** Design idea only. Not built. Parked for future development.

**Origin:** Surfaced during SFF grant application drafting (2026-04-17). The CGT tool (`cgt-skill`) is designed for grounded theory method (Charmaz 2006/2017/2020). The idea of operationalizing Hakope's Question is a distinct and valuable extension — either a standalone tool or a plugin/toggleable layer on top of the CGT tool.

Note: could be extended to all tools. 

---

## The Concept

Hakope's Question: "Did you ever consider that it isn't a bird?"

The moment in the story: June presents a queer-theory reading of archaeological debates about pre-Columbian figures — that archaeologists debating whether certain figures were "birdmen" or "birdwomen" projected European gender constructs onto the Native American past. Hakope, the community's Maker of Medicine, replies: "Did you ever consider that it isn't a bird?"

The question doesn't just redirect the answer — it rejects the frame entirely. It names that the categories themselves were the problem, not the classification within them.

**As a methodological tool:** A system that, during qualitative analysis, systematically asks: "Are we working within the right categories at all?" — not as an add-on to coding, but as a structural check that surfaces when the analytical frame itself may be importing assumptions that distort what the data can say.

---

## Possible architectures

1. **Standalone tool:** Receives coded qualitative data + emergent categories, asks Hakope's Question about each category: "Does this category come from the data, or did we bring it?" Surfaces frame-importation risk.

2. **Plugin/toggleable layer on cgt-skill:** Adds a Hakope's Question pass at key CGT stages (open coding, axial coding, theoretical saturation check). Flags when categories show evidence of researcher-frame imposition vs. data-emergence.

3. **Integration with Reframe:** Reframe already has Framework Sovereignty protocols that track suppression. Hakope's Question tool could feed into that — surfacing when the analytical framework is doing the work instead of the data.

---

## Why this matters

The CGT tool operationalizes Charmaz's constructivist integrity. Hakope's Question operationalizes the Indigenous methodological challenge to constructivism itself — the move that says: the constructivist frame is still a frame. It's the meta-level check.

Together: a CGT workflow that can ask both "are we doing this rigorously?" (Charmaz) and "are we in the right framework?" (Hakope).

---

## Next agent

- Read `cgt-skill/` to understand the existing CGT tool architecture
- Read June's description of the Hakope scene in the SFF application (`SFF/SFF_Application_Draft_iChange_v2.md`, S3) for the full narrative context
- The question is whether this is a plugin layer on cgt-skill or a standalone tool — start with plugin architecture since cgt-skill already has the pipeline
- Check with June before building: she needs to decide whether this goes into the SFF application framing
