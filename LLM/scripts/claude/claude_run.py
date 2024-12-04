import os
import time
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables from .env file
load_dotenv()
anthropic_client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

# Constants for rate-limiting
REQUEST_LIMIT = 50  # Max number of requests per minute
WAIT_TIME = 60 / REQUEST_LIMIT + 0.1 # Time to wait between requests

def claude_completion(messages, model="claude-3-5-sonnet-20241022"):
    try:
        # Extract system prompt if present
        system_prompt = ""
        if messages and messages[0]["role"] == "system":
            system_prompt = messages[0]["content"]
            messages = messages[1:]  # Remove system message from the list

        # Ensure the messages list adheres to Claude's format
        formatted_messages = []
        for message in messages:
            if message["role"] in ["user", "assistant", "system"]:
                formatted_messages.append({"role": message["role"], "content": message["content"]})

        # Make the API call
        message = anthropic_client.messages.create(
            model=model,
            system=system_prompt,
            messages=formatted_messages,
            max_tokens=2,
            temperature=0.1,
        )

        response_content = message.content[0].text.strip()

        return response_content
    
    except Exception as e:
        print(f"An error occurred with Claude: {e}")
        return None

def run_claude(messages, model):
    print(f"Processing request for model: {model}")
    response = claude_completion(messages, model=model)

    # Wait to respect rate limits
    print(f"Waiting {WAIT_TIME:.2f} seconds to respect API rate limits...")
    time.sleep(WAIT_TIME)

    return response
