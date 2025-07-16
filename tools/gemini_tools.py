# tools/gemini_tools.py
import os
import google.generativeai as genai
from crewai.tools import tool

# Configure Gemini API globally (good practice for Replit environment)
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Initialize the Gemini model once
try:
    selected_model_name = None
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            if 'flash' in m.name.lower():
                selected_model_name = m.name
                break
            elif 'pro' in m.name.lower() and not selected_model_name:
                selected_model_name = m.name
            elif not selected_model_name:
                selected_model_name = m.name

    if not selected_model_name:
        raise Exception("No Gemini model supporting 'generateContent' found with your API key.")

    print(f"Using model for GeminiTool: {selected_model_name}")
    gemini_model = genai.GenerativeModel(selected_model_name)
except Exception as e:
    print(f"Error initializing Gemini model for tool: {e}")
    gemini_model = None

@tool
def gemini_text_generator(prompt: str) -> str:
    """
    Useful for generating text, summarizing information, or answering questions using the Gemini API.
    Input should be a clear, concise natural language prompt.
    """
    if not gemini_model:
        return "Gemini model not initialized. Cannot perform text generation."
    try:
        response = gemini_model.generate_content(prompt)
        # --- ADD THESE PRINT STATEMENTS ---
        if not response:
            print("DEBUG: Gemini API returned an empty response object.")
            return "No response generated from Gemini for the given prompt."
        if not hasattr(response, 'text') or not response.text:
            print(f"DEBUG: Gemini API response has no 'text' attribute or is empty. Raw response: {response}")
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                print(f"DEBUG: Prompt Feedback (safety/blocked reasons): {response.prompt_feedback}")
            return "No text generated from Gemini for the given prompt (possibly due to safety reasons)."
        # --- END ADDED PRINT STATEMENTS ---
        return response.text
    except Exception as e:
        # This will now catch API errors
        print(f"DEBUG: Exception caught from Gemini API: {e}")
        return f"Error from Gemini API during text generation: {e}"

# You can keep the __main__ block for direct testing if you like, it's not affecting CrewAI run