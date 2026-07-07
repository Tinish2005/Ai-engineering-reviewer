import os
import json
import time
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_KEY and (GEMINI_KEY.startswith('"') or GEMINI_KEY.startswith("'")):
    GEMINI_KEY = GEMINI_KEY.strip('"').strip("'")

client = genai.Client(api_key=GEMINI_KEY)


# ------------------------------------------------------------
# 1. AI Reasoning (used by /review)
# ------------------------------------------------------------

def generate_review_reasoning(review_data: dict) -> dict:
    """Uses Gemini to explain and prioritize the review findings."""

    prompt = f"""
    You are an engineering review assistant.

    Given deterministic review data:
    Metrics, Complexity, Security, Maintainability

    Do NOT recompute metrics.

    Your job:
    1. Explain findings clearly
    2. Prioritize the most important issues
    3. Suggest actionable improvements
    4. Provide a final summary

    Return JSON with these keys:
    - "summary"
    - "priority_issues" (list)
    - "suggestions" (list)

    Analysis:
    {review_data}
    """

    attempts = 0
    response = None
    while attempts < 3:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            break
        except Exception as e:
            attempts += 1
            if attempts == 3:
                return {
                    "summary": f"Gemini reasoning error after 3 retries: {str(e)}",
                    "priority_issues": [],
                    "suggestions": []
                }
            time.sleep(2)

    text = response.text.strip()
    try:
        clean = text.strip("`")
        if clean.lower().startswith("json"):
            clean = clean[4:].strip()
        return json.loads(clean)
    except Exception:
        return {
            "summary": text,
            "priority_issues": [],
            "suggestions": []
        }


# ------------------------------------------------------------
# 2. Refactor: Corrected Code (used by /refactor and MCP tool)
# ------------------------------------------------------------

def generate_fixed_code(code: str, review_data: dict) -> str:
    """
    Uses Gemini to produce a strict, engineering-grade refactored version.
    
    Rules (mentor-approved):
    - Fix ALL reported issues in review_data
    - Do NOT rewrite logic
    - Do NOT change function names
    - Do NOT add new features
    - Return ONLY Python code (no markdown fences)
    """

    prompt = f"""
    You are a strict Python code refactoring assistant.

    Your job:
    - Fix ALL security issues reported in review_data.
    - Replace eval() with safe equivalents (ast.literal_eval or remove entirely).
    - Replace pickle.load() with json.load().
    - Replace os.system() with subprocess.run(..., shell=False) using shlex.split(cmd).
    - Reduce excessive function parameters using *args or a data class if needed.
    - Remove unresolved TODO/FIXME comments.
    - Do NOT rewrite logic.
    - Do NOT change function names.
    - Do NOT add new features.
    - Return ONLY the corrected Python code.
    - Do NOT include markdown fences.

    Original code:
    {code}

    Review data:
    {review_data}
    """

    attempts = 0
    response = None
    while attempts < 3:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            break
        except Exception as e:
            attempts += 1
            if attempts == 3:
                return f"# Error generating fixed code: {str(e)}"
            time.sleep(2)

    text = response.text.strip()

    # Clean up any Gemini markdown fences
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("python"):
            text = text[6:].strip()

    return text.strip()