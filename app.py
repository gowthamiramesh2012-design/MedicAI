from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# CORS for MIT App Inventor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load OpenAI key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

class SymptomInput(BaseModel):
    symptoms: str

@app.get("/")
def root():
    return {"status": "API running"}

@app.get("/debug-key")
def debug_key():
    return {
        "key_loaded": bool(OPENAI_API_KEY),
        "key_prefix": OPENAI_API_KEY[:3] if OPENAI_API_KEY else None
    }

@app.post("/analyze")
def analyze(data: SymptomInput):
    if not OPENAI_API_KEY:
        return {"error": "OpenAI API key not loaded"}

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"User symptoms: {data.symptoms}. Give general advice only."
            }
        ]
    )

    return {
        "result": response.choices[0].message.content
    }
