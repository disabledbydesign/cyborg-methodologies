import os
import requests
import json

# Recommended model for initial testing: Claude 3 Haiku
# It's fast, cost-effective, and capable for this task.
# You can easily swap this to a more powerful model like Sonnet or Opus later.
MODEL_NAME = "anthropic/claude-3-haiku"

# It's good practice to identify your app to the API.
# We'll use a placeholder URL as recommended by OpenRouter for local development.
YOUR_SITE_URL = "http://localhost:3000"
YOUR_APP_NAME = "cyborg-methodologies/voice-check"

def call_agent(prompt: str) -> str:
    """
    Sends a prompt to the specified model via OpenRouter and returns the response.
    """
    api_key = os.getenv("REFRAME_SHARED_OPENROUTER_KEY")
    if not api_key:
        raise ValueError("REFRAME_SHARED_OPENROUTER_KEY environment variable not set.")

    print(f"\n--- [AGENT CALL to {MODEL_NAME}] ---")
    print(f"Prompt length: {len(prompt)} characters")
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": f"{YOUR_SITE_URL}/{YOUR_APP_NAME}", # Required by OpenRouter
            },
            data=json.dumps({
                "model": MODEL_NAME,
                "max_tokens": 2048, # Explicitly set max_tokens
                "messages": [
                    {"role": "system", "content": ""},
                    {"role": "user", "content": prompt}
                ]
            })
        )

        # If the response is not OK, print the full body before raising so we can see the exact error.
        if not response.ok:
            print(f"OpenRouter error response body: {response.text}")
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        
        print(f"--- [AGENT RESPONSE RECEIVED] ---")
        return content.strip()

    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenRouter API: {e}")
        return f"Error: Could not get a response from the agent. Details: {e}"
    except (KeyError, IndexError) as e:
        print(f"Error parsing OpenRouter response: {e}")
        print(f"Full response: {response.text}")
        return f"Error: Could not parse the agent's response. Details: {e}"

