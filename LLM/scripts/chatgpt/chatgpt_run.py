from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_completion(messages, model="gpt-3.5-turbo"):
    try:
        # Use the client to create a chat completion
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1,
            temperature=0.1,
            n=1,
        )
        # Access the message content directly
        response_content = response.choices[0].message.content.strip()
        return response_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def run_chatgpt(messages, model):
    if model in ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-o1-preview"]:
        return chat_completion(messages, model=model)
    else:
        print("Invalid model specified.")
        return None
