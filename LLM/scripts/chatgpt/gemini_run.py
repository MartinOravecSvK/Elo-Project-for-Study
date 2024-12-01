import os
from dotenv import load_dotenv
from google.generativeai import client

# Load environment variables from .env file
load_dotenv()
client.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gemini_completion(messages, model="gemini-large"):
    try:
        # Use the client to create a chat completion
        response = client.chat_completions.create(
            model=model,
            messages=messages,
            max_output_tokens=1,
            temperature=0.1,
        )
        # Access the message content directly
        response_content = response["choices"][0]["message"]["content"].strip()
        return response_content
    except Exception as e:
        print(f"An error occurred with Gemini: {e}")
        return None

def run_gemini(messages, model):
    if model in ["gemini-large", "gemini-medium", "gemini-small"]:
        return gemini_completion(messages, model=model)
    else:
        print("Invalid Gemini model specified.")
        return None
