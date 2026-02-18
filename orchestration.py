import os
import json
from google import genai
from groq import Groq
from prompts import build_prompt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ✅ Read API keys properly from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ Initialize Gemini Client (new SDK)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# ✅ Initialize Groq Client
groq_client = Groq(api_key=GROQ_API_KEY)


# ---------------- GEMINI ---------------- #

def analyze_with_gemini(diff):
    prompt = build_prompt(diff)

    # response = gemini_client.models.generate_content(
    #     model="gemini-1.5-flash",
    #     contents=prompt,
    # )

    # Gemini returns text → convert to JSON safely
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            # This helps ensure the output is valid JSON
            config={'response_mime_type': 'application/json'} 
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini Error: {e}")
        return {
            "bugs": [],
            "performance": [],
            "security": [],
            "best_practices": []
        }


# ---------------- GROQ ---------------- #

def analyze_with_groq(diff):
    prompt = build_prompt(diff)
    completion = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2,
)


    try:
        return json.loads(completion.choices[0].message.content)
    except Exception:
        return {
            "bugs": [],
            "performance": [],
            "security": [],
            "best_practices": []
        }


# ---------------- ORCHESTRATION ---------------- #

def run_orchestration(diff):
    gemini_result = analyze_with_gemini(diff)
    groq_result = analyze_with_groq(diff)

    return {
        "bugs": gemini_result.get("bugs", []) + groq_result.get("bugs", []),
        "performance": gemini_result.get("performance", []) + groq_result.get("performance", []),
        "security": gemini_result.get("security", []) + groq_result.get("security", []),
        "best_practices": gemini_result.get("best_practices", []) + groq_result.get("best_practices", [])
    }
