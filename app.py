from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Symptom database
SYMPTOM_DB = {
    "fever": {
        "condition": "Possible viral or bacterial infection",
        "medicines": "Paracetamol, Ibuprofen",
        "advice": "Drink fluids and rest"
    },
    "headache": {
        "condition": "Stress, dehydration, or migraine",
        "medicines": "Paracetamol, Ibuprofen",
        "advice": "Rest and reduce screen time"
    },
    "cough": {
        "condition": "Cold, flu, or throat irritation",
        "medicines": "Cough syrup, Lozenges",
        "advice": "Warm fluids and steam inhalation"
    },
    "cold": {
        "condition": "Common cold",
        "medicines": "Antihistamines",
        "advice": "Rest and stay warm"
    },
    "sore throat": {
        "condition": "Throat infection or irritation",
        "medicines": "Lozenges, Warm salt water gargle",
        "advice": "Avoid cold drinks"
    },
    "stomach pain": {
        "condition": "Indigestion or gastritis",
        "medicines": "Antacids",
        "advice": "Avoid spicy food"
    },
    "diarrhea": {
        "condition": "Food poisoning or infection",
        "medicines": "ORS, Zinc tablets",
        "advice": "Stay hydrated"
    },
    "vomiting": {
        "condition": "Gastric infection or food poisoning",
        "medicines": "ORS, Antiemetics",
        "advice": "Small sips of water"
    },
    "chest pain": {
        "condition": "Muscle strain or heart-related issue",
        "medicines": "Consult doctor immediately",
        "advice": "Seek medical help urgently"
    },
    "shortness of breath": {
        "condition": "Asthma or respiratory infection",
        "medicines": "Inhaler if prescribed",
        "advice": "Seek medical help"
    },
    "fatigue": {
        "condition": "Weakness or viral infection",
        "medicines": "Multivitamins",
        "advice": "Adequate sleep and nutrition"
    },
    "body pain": {
        "condition": "Viral fever or muscle strain",
        "medicines": "Paracetamol",
        "advice": "Rest and warm compress"
    },
    "rash": {
        "condition": "Allergy or skin infection",
        "medicines": "Antihistamines",
        "advice": "Avoid scratching"
    },
    "dizziness": {
        "condition": "Low blood pressure or dehydration",
        "medicines": "ORS",
        "advice": "Sit or lie down immediately"
    }
}

@app.route("/")
def home():
    return "MedicAI backend running"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    symptoms_text = data.get("symptoms", "").lower()

    found = []
    for symptom, info in SYMPTOM_DB.items():
        if symptom in symptoms_text:
            found.append(info)

    if not found:
        return jsonify({
            "result": "Condition: Unknown\nMedicines: Consult doctor\nAdvice: Please seek medical attention\n\n⚠️ This is general information and not a medical diagnosis."
        })

    condition = ", ".join(set(i["condition"] for i in found))
    medicines = ", ".join(set(i["medicines"] for i in found))
    advice = ", ".join(set(i["advice"] for i in found))

    return jsonify({
        "result": f"""Condition:
{condition}

Medicines:
{medicines}

Advice:
{advice}

⚠️ This is general information and not a medical diagnosis."""
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
