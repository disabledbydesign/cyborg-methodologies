"""
Generates the 'story pass' — raw, voice-forward argumentative material 
without genre constraints.
"""

from agent_caller import call_agent

def generate():
    """
    Generates the story pass content by calling an agent
    with a detailed, context-rich prompt.
    """
    print("Generating story pass via agent call...")

    # --- 1. Gather Context (Simulated) ---
    # In a real run, you would load these from files.
    job_posting = "Seeking a UX Researcher to improve developer tool adoption..."
    voice_document = "My voice is direct, analytical, and uses precise data. I build systems to make arguments..."
    research_notes = "The GitLab analysis showed that framing is key. The trust paradox (29% vs 84%) is a powerful anchor..."

    # --- 2. Build the Prompt from the Spec ---
    prompt = f"""
    You are an expert writing assistant. Your task is to generate a "story pass" for a cover letter.
    This is not a draft. It is raw, voice-forward argumentative material that will be restructured later.

    Follow these rules precisely:
    1.  **Find the Argument:** Read the provided documents and find the core argument. Why is this person the right fit for this specific job?
    2.  **No Genre Constraints:** Do not use cover letter formatting. No headers, no salutation. Write in a first-person, narrative style.
    3.  **Anchor Claims:** Every claim must be anchored in a specific detail from the documents (a number, a named finding, a specific community).
    4.  **Use [DATA NEEDED]:** If you need a specific fact to make a claim but don't have it, write `[DATA NEEDED: describe what you need]` instead of making a vague statement.
    5.  **Voice:** The tone should reflect the provided voice document: direct, analytical, and focused on building systems.

    Here is the context:

    **Job Posting:**
    {job_posting}

    **Voice Document:**
    {voice_document}

    **Research Notes:**
    {research_notes}

    Now, generate the story pass.
    """

    # --- 3. Call the Agent ---
    story_pass_output = call_agent(prompt)
    return story_pass_output
