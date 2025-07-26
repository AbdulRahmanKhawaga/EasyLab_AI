from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import os
import pandas as pd
import json

# FastAPI application for machine learning model inference
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust if needed for deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load resources
scaler = joblib.load("best_model_scaler.pkl")
label_encoder = joblib.load("best_model_label_encoder.pkl")

# Load top features to ensure correct column order
with open("top_features.json", "r") as f:
    top_features = json.load(f)

# Load model
if os.path.exists("best_model_sklearn.pkl"):
    model_type = "sklearn"
    model = joblib.load("best_model_sklearn.pkl")
elif os.path.exists("best_model_ann.h5"):
    from tensorflow.keras.models import load_model
    model_type = "ANN"
    model = load_model("best_model_ann.h5")
else:
    raise Exception("No valid model file found!")

# Input model
class CBCInput(BaseModel):
    hgb: float
    mcv: float
    mchc: float
    wbc: float
    rbc: float
    platelets: float
    hct: float
    mch: float

@app.post("/api/diagnose")
def diagnose(input_data: CBCInput):
    try:
        input_dict = {
            "HGB": input_data.hgb,
            "MCV": input_data.mcv,
            "MCHC": input_data.mchc,
            "WBC": input_data.wbc,
            "RBC": input_data.rbc,
            "PLT": input_data.platelets,
            "HCT": input_data.hct,
            "MCH": input_data.mch,
        }

        # Reorder DataFrame columns to match training
        features = pd.DataFrame([input_dict])[top_features]

        print("Raw input:", features)

        scaled_features = scaler.transform(features)
        print("Scaled input:", scaled_features)

        if model_type == "ANN":
            probs = model.predict(scaled_features)[0]
        else:
            probs = model.predict_proba(scaled_features)[0]

        prediction_index = np.argmax(probs)
        prediction_label = label_encoder.inverse_transform([prediction_index])[0]
        confidence = float(probs[prediction_index])

        print("Model probs:", probs)
        print("Chosen index:", prediction_index)
        print("Decoded label:", prediction_label)

        return {
            "diagnosis": prediction_label,
            "confidence": round(confidence, 4)
        }

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "FastAPI ML API is running"}
