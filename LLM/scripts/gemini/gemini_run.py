import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, InternalServerError

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gemini_completion(messages, model_name="gemini-1.5-pro", max_retries=8):
    try:
        # Initialize the GenerativeModel with the specified model name
        model = genai.GenerativeModel(model_name)
        
        # Prepare the prompt by concatenating user messages
        prompt = "\n".join([msg["content"] for msg in messages if msg["role"] == "user"])
        
        # Implement exponential backoff
        for attempt in range(max_retries):
            try:
                # Generate content using the model
                response = model.generate_content(prompt)

                # Access the generated text
                response_content = response.text.split("\n")[-2]
                # response_content = str(response.text.strip())
                return response_content
            except ResourceExhausted as e:
                # Handle rate limit exceeded error
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            except InternalServerError as e:
                # Handle internal server errors
                print(f"Internal server error: {e}. Retrying...")
                time.sleep(2 ** attempt)
        print("Max retries exceeded. Request failed.")
        return None
    except Exception as e:
        print(f"An error occurred with Gemini: {e}")
        return None

def run_gemini(messages, model_name="gemini-1.5-pro"):
    if model_name in ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.5-flash-8b"]:
        return gemini_completion(messages, model_name=model_name)
    else:
        print("Invalid Gemini model specified.")
        return None
