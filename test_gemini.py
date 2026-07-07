import os
from dotenv import load_dotenv
from google import genai

# Load env
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Strip quotes if present
if GEMINI_KEY and (GEMINI_KEY.startswith('"') or GEMINI_KEY.startswith("'")):
    GEMINI_KEY = GEMINI_KEY.strip('"').strip("'")

# Initialize Gemini
client = genai.Client(api_key=GEMINI_KEY)

# Test prompt
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="Reply with a short greeting and tell me you are working."
)

print("✅ Gemini Response:")
print(response.text)