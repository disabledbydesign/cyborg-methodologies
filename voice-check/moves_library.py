"""
A library of named rhetorical moves for the reorganization pass.
"""

# This represents the 'tech_position' moves from the spec.
# In a real system, this might be loaded from a YAML or JSON file.
MOVES_LIBRARY = {
    "tech_position": {
        "successful": [
            {
                "name": "Problem-Data Bridge",
                "description": "Opens with a concrete problem + data, reframed as a design problem.",
                "when": "Tech roles where the posting doesn't name the real need; when you have diagnostic insight the posting missed.",
                "example": "Developer trust has dropped to 29% even as adoption has risen to 84% — that is not a training data problem. It is a knowledge construction problem."
            },
            {
                "name": "System-Builder as Researcher",
                "description": "Establishes candidate as someone who produced findings by building, not by observing.",
                "when": "Need to distinguish from pure-research or pure-engineering candidates; when the tool IS the methodology.",
                "example": "I rebuilt the classifier as a four-axis system. Research drove the architectural change."
            }
        ],
        "abandoned": [
            {
                "name": "Problem-Pedagogy Opening",
                "description": "Opens by explaining the psychology or mechanism of a problem in detail, before establishing why the candidate is the solver.",
                "what_failed": "Explained trust as 'cognitive operations...' — explained without positioning."
            }
        ]
    }
}

def get_moves_for_genre(genre):
    """
    Retrieves the successful moves for a given genre.
    """
    return MOVES_LIBRARY.get(genre, {}).get("successful", [])

def get_all_moves():
    """
    Returns the entire moves library.
    """
    return MOVES_LIBRARY
