import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

models = genai.list_models()
with open("models.log", "w") as f:
    for m in models:
        f.write(f"{m.name}\n")
print("Models saved.")
