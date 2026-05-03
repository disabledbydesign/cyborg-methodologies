"""
Pilot script for Experiments 2 and 3.

This script runs both the current and the new two-pass pipeline to compare
their outputs (Experiment 3: Story Pass A/B Test).

It also allows for testing different prompt framings for the qualitative
checks in the new pipeline (Experiment 2: Prompt Framing Test).
"""

import argparse
import os
import shutil
from dotenv import load_dotenv
import run_current_pipeline
import run_new_pipeline
import outline_pass

OUTPUT_DIR = "outputs"

def setup_output_dir():
    """Create a clean directory for experiment outputs."""
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

def save_output(filename, content):
    """Save content to a file in the output directory."""
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved output to {path}")

def run_experiment_3():
    """Runs the A/B test comparing the current pipeline with the new ones."""
    setup_output_dir()
    print("--- Running Experiment 3: All Workflows A/B/C/D Test ---")
    
    # --- Draft A: Current Pipeline ---
    print("\n\n=> Generating Draft A (Current Pipeline):")
    draft_a = run_current_pipeline.run()
    save_output("A_current_pipeline.md", draft_a)
    
    # --- Draft B: Story -> Draft ---
    print("\n\n=> Generating Draft B (Story -> Draft):")
    draft_b = run_new_pipeline.run(workflow="story-to-draft")
    save_output("B_story_to_draft.md", draft_b)
    
    # --- Draft C: Outline -> Draft ---
    print("\n\n=> Generating Draft C (Outline -> Draft):")
    draft_c = run_new_pipeline.run(workflow="outline-to-draft")
    save_output("C_outline_to_draft.md", draft_c)

    # --- Draft D: Story -> Outline -> Draft ---
    print("\n\n=> Generating Draft D (Story -> Outline -> Draft):")
    draft_d = run_new_pipeline.run(workflow="story-to-outline-to-draft")
    save_output("D_story_to_outline_to_draft.md", draft_d)
    
    print("\n\n--- Comparison ---")
    print(f"All drafts have been saved to the '{OUTPUT_DIR}' directory.")
    
    print("\nExperiment 3 complete. Review the generated markdown files.")

def run_experiment_2():
    """Runs the prompt framing test."""
    setup_output_dir()
    print("--- Running Experiment 2: Prompt Framing Test ---")
    
    framings = ["control", "motivation-framed", "welfare-aware"]
    drafts = {}
    
    for framing in framings:
        print(f"\n=> Generating draft with '{framing}' framing:")
        drafts[framing] = run_new_pipeline.run(prompt_framing=framing)
        save_output(f"exp2_{framing}_draft.md", drafts[framing])
        
    print("\n\n--- Comparison ---")
    print(f"All drafts have been saved to the '{OUTPUT_DIR}' directory.")
        
    print("\nExperiment 2 complete. Review the generated markdown files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pipeline experiments.")
    parser.add_argument(
        'experiment', 
        choices=['exp2', 'exp3'], 
        help="The experiment to run: 'exp2' for Prompt Framing Test, 'exp3' for Story Pass A/B Test."
    )
    parser.add_argument(
        '--env-file',
        help="Path to the .env file containing the OPENROUTER_API_KEY."
    )
    args = parser.parse_args()

    # Load the environment variables from the specified file
    if args.env_file:
        if os.path.exists(args.env_file):
            load_dotenv(dotenv_path=args.env_file)
            print(f"Loaded environment variables from {args.env_file}")
        else:
            print(f"Warning: specified --env-file '{args.env_file}' not found.")

    if args.experiment == 'exp2':
        run_experiment_2()
    elif args.experiment == 'exp3':
        run_experiment_3()
