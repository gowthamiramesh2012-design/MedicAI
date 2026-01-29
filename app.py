from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    return {
        "result": f"""Condition:
Possible Viral Infection

Medicines:
Paracetamol, ORS

Advice:
Rest well and consult a doctor if symptoms persist.

⚠️ This is general information and not a medical diagnosis."""
    }
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

return {
    "result": response.choices[0].message.content
}
