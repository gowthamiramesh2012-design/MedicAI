from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# CORS (MIT App Inventor friendly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load OpenAI key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)


class SymptomInput(BaseModel):
    symptoms: str


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/debug-key")
def debug_key():
    return {
        "openai_key_loaded": bool(OPENAI_API_KEY),
        "key_prefix": OPENAI_API_KEY[:3] if OPENAI_API_KEY else None
    }


@app.post("/analyze")
def analyze(data: SymptomInput):
    if not data.symptoms:
        raise HTTPException(status_code=400, detail="Symptoms missing")

    # If OpenAI key is missing, return fallback (NO crash)
    if not client:
        return {
            "result": f"""
Condition:
Unknown (AI unavailable)

Symptoms:
{data.symptoms}

Advice:
Rest, fluids, consult a doctor if symptoms persist.

⚠️ OpenAI key not configured.
"""
        }

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical assistant. Give general advice only."
                },
                {
                    "role": "user",
                    "content": f"My symptoms are: {data.symptoms}"
                }
            ],
            max_tokens=200
        )

        return {
            "result": response.choices[0].message.content
        }

    except Exception as e:
        # Catch EVERYTHING so FastAPI never returns 500
        return {
            "result": f"""
Condition:
Unable to analyze

Symptoms:
{data.symptoms}

Error:
{str(e)}

⚠️ AI service error. Not a medical diagnosis.
"""
                            }
