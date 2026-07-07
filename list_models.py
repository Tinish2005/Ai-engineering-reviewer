import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_KEY and (GEMINI_KEY.startswith('"') or GEMINI_KEY.startswith("'")):
    GEMINI_KEY = GEMINI_KEY.strip('"').strip("'")

client = genai.Client(api_key=GEMINI_KEY)

models = client.models.list()
for m in models:
    print(m.name)