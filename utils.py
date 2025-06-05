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

# Function to list available models (for debugging)
def list_available_models():
    try:
        models = genai.list_models()
        available_models = [model.name for model in models]
        return available_models
    except Exception as e:
        return f"Error listing models: {str(e)}"

# Initialize the model with fallbacks
def get_model():
    model_options = [
        "models/gemini-pro",       # Try with full path format
        "gemini-pro",              # Try without path prefix
        "models/gemini-1.0-pro",   # Try alternate naming convention
        "gemini-1.0-pro"           # Try alternate without prefix
    ]
    
    for model_name in model_options:
        try:
            model = genai.GenerativeModel(model_name)
            # Test the model with a simple prompt
            response = model.generate_content("Hello")
            print(f"Successfully connected using model: {model_name}")
            return model
        except Exception as e:
            print(f"Failed to initialize {model_name}: {str(e)}")
            continue
    
    # If all attempts fail, raise exception
    raise ValueError("Unable to initialize any Gemini model. Please check your API key and network connection.")

# Get a working model instance
try:
    model = get_model()
except Exception as e:
    print(f"Model initialization failed: {str(e)}")
    # Will be handled in ask_question function

# Function to ask a question
def ask_question(question: str) -> str:
    try:
        # Try to ensure model is initialized
        if 'model' not in globals():
            try:
                global model
                model = get_model()
            except Exception as e:
                return f"❌ Could not initialize model: {str(e)}"
        
        prompt = f"""
        Please answer the following academic question comprehensively and accurately:
        
        {question}
        
        Provide a clear explanation suitable for an educational context.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg and "quota" in error_msg:
            return "❌ API rate limit exceeded. Please try again in a few minutes or contact the administrator to upgrade the API plan."
        elif "403" in error_msg:
            return "❌ Authentication error. Please check the API key configuration."
        elif "404" in error_msg:
            available_models = list_available_models()
            return f"❌ Model not found. Available models: {available_models}"
        else:
            return f"❌ Error occurred: {error_msg}"