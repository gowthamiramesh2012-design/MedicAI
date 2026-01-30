from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SymptomInput(BaseModel):
    symptoms: str

@app.get("/health")
def health():
    return {
        "openai_key_loaded": bool(os.getenv("OPENAI_API_KEY"))
    }

@app.post("/analyze")
def analyze(data: SymptomInput):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    prompt = f"""
You are a medical assistant AI.

User symptoms:
{data.symptoms}

Respond ONLY in this format:

Condition:
Medicines:
Advice:

Add this line at the end:
"⚠️ This is general information and not a medical diagnosis."
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )

    return {
        "result": response.choices[0].message.content
    }
