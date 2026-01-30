from fastapi import FastAPI
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
    return {"openai_key_loaded": bool(os.getenv("OPENAI_API_KEY"))}

@app.post("/analyze")
def analyze(data: SymptomInput):
    prompt = f"""
User symptoms: {data.symptoms}

Give:
1. Possible condition
2. Basic medicines
3. Advice

Short and clear.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "result": response.choices[0].message.content
    }
