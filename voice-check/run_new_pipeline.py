"""
Orchestrates the new two-pass writing pipeline.
1. Story Pass: Generates raw argumentative material.
2. Reorganization Pass: Applies genre structure using a moves library.
"""

import story_pass
import reorganization_pass
import moves_library
import outline_pass

def run(workflow="story-to-draft", prompt_framing="motivation-framed"):
    """
    Runs the two-pass pipeline using a specified workflow.

    Args:
        workflow (str): The drafting workflow to use. One of:
                        'story-to-draft', 'outline-to-draft', 'story-to-outline-to-draft'.
        prompt_framing (str): The framing to use for qualitative checks.
                              "control", "motivation-framed", or "welfare-aware".
    """
    print(f"Running the new pipeline with workflow: {workflow}...")

    # --- Stage 1: Initial Content/Structure Generation ---
    if workflow == 'story-to-draft':
        print("\n--- Starting Story Pass ---")
        intermediate_material = story_pass.generate()
        print("Story Pass generated:", intermediate_material)
    elif workflow == 'outline-to-draft':
        print("\n--- Starting Outline Pass (De Novo) ---")
        intermediate_material = outline_pass.generate()
        print("De Novo Outline generated:", intermediate_material)
    elif workflow == 'story-to-outline-to-draft':
        print("\n--- Starting Story Pass ---")
        story_material = story_pass.generate()
        print("Story Pass generated:", story_material)
        print("\n--- Starting Outline Pass (from Story) ---")
        intermediate_material = outline_pass.generate(source_material=story_material)
        print("Outline from Story generated:", intermediate_material)
    else:
        raise ValueError(f"Unknown workflow: {workflow}")


    # --- Stage 2: Reorganization/Drafting Pass ---
    print("\n--- Starting Reorganization Pass ---")
    
    # In a real scenario, the agent would select moves based on the intermediate material.
    # Here, we'll just grab the first available move for demonstration.
    moves = moves_library.get_moves_for_genre("tech_position")
    selected_move = moves[0] if moves else None
    
    print(f"Selected move: {selected_move['name'] if selected_move else 'None'}")

    final_draft = reorganization_pass.reorganize(
        intermediate_material, 
        selected_move,
        prompt_framing=prompt_framing
    )
    print("Reorganization Pass generated:", final_draft)
    
    print("\nNew pipeline draft generation complete.")
    return final_draft

if __name__ == "__main__":
    run()
