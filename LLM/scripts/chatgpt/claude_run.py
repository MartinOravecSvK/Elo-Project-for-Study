import os
from dotenv import load_dotenv
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Load environment variables from .env file
load_dotenv()
anthropic_client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def claude_completion(messages, model="claude-v1"):
    try:
        conversation = ""
        for message in messages:
            role = HUMAN_PROMPT if message["role"] == "user" else AI_PROMPT
            conversation += f"{role} {message['content']}"
        response = anthropic_client.completions.create(
            model=model,
            prompt=conversation,
            max_tokens_to_sample=1,
            temperature=0.1,
        )
        response_content = response["completion"].strip()
        return response_content
    except Exception as e:
        print(f"An error occurred with Claude: {e}")
        return None

def run_claude(messages, model):
    if model in ["claude-v1", "claude-v1.3", "claude-v2"]:
        return claude_completion(messages, model=model)
    else:
        print("Invalid Claude model specified.")
        return None
