# simple_gemini_test.py
import os
import google.generativeai as genai

# Ensure GOOGLE_API_KEY is set in your environment or Replit secrets
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

try:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content("Tell me a fun fact about giraffes.")
    print("Gemini API call successful! Response:")
    print(response.text)
except Exception as e:
    print(f"Gemini API call failed: {e}")