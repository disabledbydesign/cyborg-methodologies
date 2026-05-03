"""
The reorganization pass applies genre structure to the story pass output
using a selected move from the moves library.
"""

def reorganize(story_material, move, prompt_framing="motivation-framed"):
    """
    Reshapes the story material into a structured draft.

    Args:
        story_material (str): The output from the story_pass.
        move (dict): The selected move from the moves_library.
        prompt_framing (str): The framing for qualitative checks.

    Returns:
        str: A structured draft.
    """
    print(f"Reorganizing material using move: '{move['name']}' with '{prompt_framing}' framing.")
    
    # This is a placeholder for the logic that would use an LLM to
    # restructure the story_material according to the selected move.
    # The implementation would be a prompt that includes the story material,
    # the move's description and examples, and the qualitative check instructions
    # framed according to the 'prompt_framing' parameter.

    # For this pilot, we'll just combine the move's example with the story material
    # to simulate the output.
    
    if not move:
        return f"FAIL: No move selected. Raw material: {story_material}"

    # Simulate applying the move's logic.
    # A real implementation would be much more sophisticated.
    reorganized_draft = f"({move['name']} Opening): {move['example']}\n\n{story_material}"

    # Placeholder for running the qualitative check protocol
    print(f"Running qualitative checks with {prompt_framing} framing...")
    # ... qualitative check logic would go here ...
    print("Qualitative checks passed (simulated).")

    return reorganized_draft
