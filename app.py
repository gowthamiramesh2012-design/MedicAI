from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# CORS (for MIT App Inventor)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SymptomInput(BaseModel):
    symptoms: str

@app.get("/")
def home():
    return {"status": "MedicAI backend running"}

@app.get("/health")
def health():
    return {
        "openai_key_loaded": bool(os.getenv("OPENAI_API_KEY"))
    }

@app.post("/analyze")
def analyze(data: SymptomInput):
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
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )

    return {
        "result": response.choices[0].message.content
    }

