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

openai.api_key = os.getenv("OPENAI_API_KEY")

class SymptomInput(BaseModel):
    symptoms: str

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

Add this line at the end:
"⚠️ This is general information and not a medical diagnosis."
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return {
        "result": response.choices[0].message.content
    }

@app.get("/")
def home():
    return {"status": "MedicAI AI backend running"}
