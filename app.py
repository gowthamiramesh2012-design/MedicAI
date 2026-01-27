from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Allow MIT App Inventor access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 OpenAI API Key (set in Render)
openai.api_key = os.getenv("OPENAI_API_KEY")

class SymptomInput(BaseModel):
    symptoms: str

@app.post("/analyze")
def analyze(symptoms: SymptomInput):
    prompt = f"""
You are a medical assistant AI.

User symptoms:
{symptoms.symptoms}

Respond ONLY in this format:

Condition:
Medicines:
Advice:

Keep it short, clear, and safe.
Add a disclaimer line at the end.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    result = response.choices[0].message.content

    return {
        "result": result
    }

@app.get("/")
def home():
    return {"status": "MedicAI AI backend running"}

@app.get("/analyze")
def analyze(symptoms: str):
    return {
        "condition": "Possible Viral Infection",
        "medicines": "Paracetamol, ORS",
        "advice": "Rest well and consult a doctor if symptoms persist"
    }

