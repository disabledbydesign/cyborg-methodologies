"""
Generates a structured outline.
"""

def generate(source_material=None):
    """
    Generates an outline.

    If source_material is provided (e.g., from a story pass), it generates
    an outline based on that material. Otherwise, it creates a de novo outline.

    For this pilot, we return a hardcoded string.
    """
    if source_material:
        print("Generating outline from story pass material...")
        # In a real implementation, an LLM would structure the source material.
        return (
            "1. **Opening (Problem-Data Bridge):** Start with the 29%/84% trust/adoption statistic to frame the knowledge construction problem.\n"
            "2. **Core Competency (System-Builder as Researcher):** Detail the four-axis classifier as proof of turning research into architecture.\n"
            "3. **Application (Problem Instance Serialization):** Show how this insight applies to Duo, Knowledge Graph, and Marketplace.\n"
            "4. **Credibility (Credentialing-by-Community):** Mention Carter Center/NCCHR work to ground the expertise."
        )
    else:
        print("Generating de novo outline...")
        # In a real implementation, an LLM would create this from the job posting.
        return (
            "1. **Introduction:** State interest in the role.\n"
            "2. **Point 1:** Connect research background to the company's main product.\n"
            "3. **Point 2:** Provide an example of building a system.\n"
            "4. **Conclusion:** Reiterate fit and call to action."
        )
