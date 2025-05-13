from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Validate API key
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file.")

# Configure the Gemini API client
genai.configure(api_key=api_key)

# Correct usage of the REST-based model name
model = genai.GenerativeModel("gemini-pro")  # ✅ DO NOT prefix with "models/"

# Function to ask a question
def ask_question(question: str) -> str:
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"❌ Error occurred: {str(e)}"
