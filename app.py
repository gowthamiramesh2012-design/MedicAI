from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

# ----------------------------
# App setup
# ----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# OpenAI client
# ----------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# ----------------------------
# Request model
# ----------------------------
class SymptomInput(BaseModel):
    symptoms: str

# ----------------------------
# Health check
# ----------------------------
@app.get("/health")
def health():
    return {
        "openai_key_loaded": bool(OPENAI_API_KEY)
    }

# ----------------------------
# Debug endpoint (temporary)
# ----------------------------
@app.get("/debug")
def debug():
    return {
        "key_loaded": bool(OPENAI_API_KEY),
        "key_preview": OPENAI_API_KEY[:8] + "..." if OPENAI_API_KEY else None
    }

# ----------------------------
# Analyze symptoms
# ----------------------------
@app.post("/analyze")
def analyze(data: SymptomInput):
    if not OPENAI_API_KEY:
        return {"error": "OPENAI_API_KEY not loaded"}

    prompt = f"""
You are a medical assistant AI.

User symptoms:
{data.symptoms}

Respond ONLY in this format:

Condition:
Medicines:
Advice:

⚠️ This is general information and not a medical diagnosis.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    return {
        "result": response.choices[0].message.content
    }

# ----------------------------
# Root
# ----------------------------
@app.get("/")
def root():
    return {"status": "MedicAI backend running"}

