from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

DISCLAIMER = (
    "This app provides general health information only. "
    "It does NOT diagnose or replace a medical professional. "
    "Consult a doctor for proper treatment."
)

DATABASE = {
    "fever": {
        "conditions": ["Viral Fever", "Flu", "Infection"],
        "medicines": ["Paracetamol", "Ibuprofen"],
        "advice": "Rest, fluids. Doctor if fever > 2 days."
    },
    "cold": {
        "conditions": ["Common Cold", "Allergy"],
        "medicines": ["Cetirizine", "Levocetirizine"],
        "advice": "Avoid cold drinks."
    },
    "cough": {
        "conditions": ["Dry Cough", "Chest Infection"],
        "medicines": ["Dextromethorphan", "Bromhexine"],
        "advice": "Doctor if cough > 7 days."
    },
    "headache": {
        "conditions": ["Tension Headache", "Migraine"],
        "medicines": ["Paracetamol"],
        "advice": "Rest, hydration."
    },
    "stomach pain": {
        "conditions": ["Acidity", "Indigestion"],
        "medicines": ["Omeprazole", "Gelusil"],
        "advice": "Avoid spicy food."
    },
    "diarrhea": {
        "conditions": ["Food Poisoning", "Infection"],
        "medicines": ["ORS", "Zinc"],
        "advice": "Hydration is critical."
    },
    "vomiting": {
        "conditions": ["Gastritis", "Food Poisoning"],
        "medicines": ["ORS", "Domperidone"],
        "advice": "Small sips of water."
    },
    "sore throat": {
        "conditions": ["Throat Infection"],
        "medicines": ["Warm Gargle", "Paracetamol"],
        "advice": "Avoid cold food."
    },
    "body pain": {
        "conditions": ["Muscle Strain", "Viral Infection"],
        "medicines": ["Paracetamol"],
        "advice": "Rest and hydration."
    },
    "back pain": {
        "conditions": ["Muscle Strain"],
        "medicines": ["Paracetamol"],
        "advice": "Avoid heavy lifting."
    },
    "allergy": {
        "conditions": ["Seasonal Allergy"],
        "medicines": ["Cetirizine"],
        "advice": "Avoid allergens."
    },
    "acidity": {
        "conditions": ["GERD"],
        "medicines": ["Omeprazole"],
        "advice": "Eat small meals."
    },
    "asthma": {
        "conditions": ["Asthma"],
        "medicines": ["Salbutamol Inhaler"],
        "advice": "Emergency care if breathing worsens."
    },
    "burn": {
        "conditions": ["Minor Burn"],
        "medicines": ["Cool Water", "Burn Ointment"],
        "advice": "Hospital for severe burns."
    },
    "cut": {
        "conditions": ["Minor Injury"],
        "medicines": ["Antiseptic", "Bandage"],
        "advice": "Clean wound properly."
    },
    "toothache": {
        "conditions": ["Dental Infection"],
        "medicines": ["Paracetamol"],
        "advice": "Visit dentist ASAP."
    },
    "ear pain": {
        "conditions": ["Ear Infection"],
        "medicines": ["Paracetamol"],
        "advice": "Do not insert objects."
    },
    "eye irritation": {
        "conditions": ["Eye Allergy"],
        "medicines": ["Lubricating Eye Drops"],
        "advice": "Avoid rubbing eyes."
    },
    "constipation": {
        "conditions": ["Digestive Issue"],
        "medicines": ["Isabgol"],
        "advice": "Increase fiber intake."
    },
    "insomnia": {
        "conditions": ["Sleep Disorder"],
        "medicines": ["Sleep Hygiene"],
        "advice": "Avoid screens at night."
    }
}

EMERGENCY_SYMPTOMS = [
    "chest pain", "breathing difficulty", "unconscious",
    "severe bleeding", "seizure"
]

@app.get("/")
def home():
    return {"status": "server alive"}

@app.get("/suggest")
def suggest(symptoms: str = Query(None)):
    if symptoms is None or symptoms.strip() == "":
        return JSONResponse(
            {"error": "No symptoms provided"},
            status_code=400
        )

    return {
    "result": (
        "Possible condition: Viral Fever\n"
        "Medicines: Paracetamol, ORS\n"
        "Advice: Rest, drink fluids, consult doctor if persists"
    )
}

