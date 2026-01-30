import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# Load OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set")

client = OpenAI(api_key=api_key)

class SymptomRequest(BaseModel):
    symptoms: str

@app.get("/")
def root():
    return {"status": "MedicAI backend running"}

@app.get("/health")
def health():
    return {"openai_key_loaded": True}

@app.post("/analyze")
def analyze(data: SymptomRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical assistant. Provide general health guidance, not a diagnosis."
                },
                {
                    "role": "user",
                    "content": data.symptoms
                }
            ],
            temperature=0.4
        )

        # THIS is the part people forget
        result = response.choices[0].message.content

        return {
            "symptoms": data.symptoms,
            "analysis": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
