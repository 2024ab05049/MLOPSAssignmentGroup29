"""
FastAPI application for Heart Disease Prediction Model
Deployed on Azure App Service
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import numpy as np
import pandas as pd
from joblib import load
import os
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(
    title="Heart Disease Prediction API",
    description="MLOps Assignment - Group 29: Heart Disease Risk Prediction",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input schema
class HeartDiseaseInput(BaseModel):
    age: float = Field(..., description="Age in years")
    sex: int = Field(..., description="Sex (0=female, 1=male)")
    cp: int = Field(..., description="Chest pain type (0-3)")
    trestbps: float = Field(..., description="Resting blood pressure")
    chol: float = Field(..., description="Serum cholesterol in mg/dl")
    fbs: int = Field(..., description="Fasting blood sugar > 120 mg/dl (0=no, 1=yes)")
    restecg: int = Field(..., description="Resting electrocardiographic results (0-2)")
    thalach: float = Field(..., description="Maximum heart rate achieved")
    exang: int = Field(..., description="Exercise induced angina (0=no, 1=yes)")
    oldpeak: float = Field(..., description="ST depression induced by exercise")
    slope: int = Field(..., description="Slope of peak exercise ST segment (0-2)")
    ca: float = Field(..., description="Number of major vessels colored by flourosopy")
    thal: int = Field(..., description="Thalassemia (0-3)")

    class Config:
        schema_extra = {
            "example": {
                "age": 63,
                "sex": 1,
                "cp": 3,
                "trestbps": 145,
                "chol": 233,
                "fbs": 1,
                "restecg": 0,
                "thalach": 150,
                "exang": 0,
                "oldpeak": 2.3,
                "slope": 0,
                "ca": 0,
                "thal": 1
            }
        }

class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="Predicted class (0=no disease, 1=disease)")
    probability: float = Field(..., description="Probability of disease")
    model_used: str = Field(..., description="Model used for prediction")

# Global model variables
model_lr = None
model_rf = None
MODEL_TYPE = os.getenv("MODEL_TYPE", "logreg")  # Default to logistic regression

def load_model():
    """Load the trained model"""
    global model_lr, model_rf
    
    # Try to load from different possible paths
    model_paths = [
        Path("models/best_logreg_pipeline.joblib"),
        Path("models/logreg_cv_best_pipeline.joblib"),
        Path("models/best_randomforest_pipeline.joblib"),
        Path("models/rf_cv_best_pipeline.joblib"),
    ]
    
    # Also check Azure App Service default paths
    if os.getenv("WEBSITE_SITE_NAME"):
        # Running on Azure
        base_path = Path("/home/site/wwwroot")
        model_paths.extend([
            base_path / "models/best_logreg_pipeline.joblib",
            base_path / "models/logreg_cv_best_pipeline.joblib",
            base_path / "models/best_randomforest_pipeline.joblib",
            base_path / "models/rf_cv_best_pipeline.joblib",
        ])
    
    # Load models
    for path in model_paths:
        if path.exists():
            try:
                if "logreg" in path.name.lower():
                    model_lr = load(path)
                    print(f"Loaded Logistic Regression model from {path}")
                elif "randomforest" in path.name.lower() or "rf" in path.name.lower():
                    model_rf = load(path)
                    print(f"Loaded Random Forest model from {path}")
            except Exception as e:
                print(f"Error loading {path}: {e}")
    
    if model_lr is None and model_rf is None:
        raise FileNotFoundError("No model files found. Please ensure model files are in the models/ directory.")

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        load_model()
        print("Models loaded successfully!")
    except Exception as e:
        print(f"Error loading models: {e}")
        print("API will start but predictions will fail until models are available.")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Heart Disease Prediction API",
        "status": "running",
        "model_loaded": model_lr is not None or model_rf is not None,
        "model_type": MODEL_TYPE
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model_lr is not None or model_rf is not None
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: HeartDiseaseInput):
    """
    Predict heart disease risk
    
    Returns:
    - prediction: 0 (no disease) or 1 (disease present)
    - probability: Probability of disease (0-1)
    - model_used: Which model was used for prediction
    """
    try:
        # Convert input to pandas DataFrame in the correct order
        # Match exact format from training
        NUMERIC_COLS = ['age','trestbps','chol','thalach','oldpeak','ca']
        CATEGORICAL_COLS = ['sex','cp','fbs','restecg','exang','slope','thal']
        feature_names = NUMERIC_COLS + CATEGORICAL_COLS
        
        # Create DataFrame exactly as in training (list of lists with columns)
        features = pd.DataFrame([[
            float(input_data.age),
            int(input_data.sex),
            int(input_data.cp),
            float(input_data.trestbps),
            float(input_data.chol),
            int(input_data.fbs),
            int(input_data.restecg),
            float(input_data.thalach),
            int(input_data.exang),
            float(input_data.oldpeak),
            int(input_data.slope),
            float(input_data.ca),
            int(input_data.thal)
        ]], columns=feature_names)
        
        # Ensure correct dtypes (match training exactly)
        for c in NUMERIC_COLS:
            features[c] = pd.to_numeric(features[c], errors='coerce')
        for c in CATEGORICAL_COLS:
            features[c] = pd.to_numeric(features[c], errors='coerce')
        
        # Select model based on MODEL_TYPE env variable or availability
        model = None
        model_name = ""
        
        if MODEL_TYPE.lower() in ["logreg", "logistic", "lr"]:
            if model_lr is not None:
                model = model_lr
                model_name = "logistic_regression"
            elif model_rf is not None:
                model = model_rf
                model_name = "random_forest"
        else:
            if model_rf is not None:
                model = model_rf
                model_name = "random_forest"
            elif model_lr is not None:
                model = model_lr
                model_name = "logistic_regression"
        
        if model is None:
            raise HTTPException(
                status_code=503,
                detail="No model available. Please ensure model files are loaded."
            )
        
        # Debug: Check features type and shape
        print(f"DEBUG: Features type: {type(features)}, shape: {features.shape if hasattr(features, 'shape') else 'N/A'}")
        print(f"DEBUG: Is DataFrame: {isinstance(features, pd.DataFrame)}")
        if isinstance(features, pd.DataFrame):
            print(f"DEBUG: DataFrame columns: {list(features.columns)}")
            print(f"DEBUG: DataFrame dtypes:\n{features.dtypes}")
        
        # Make prediction - ensure we're working with a fresh DataFrame copy
        features_copy = features.copy()
        print(f"DEBUG: After copy - type: {type(features_copy)}, is DataFrame: {isinstance(features_copy, pd.DataFrame)}")
        
        # Try prediction
        try:
            prediction = model.predict(features_copy)[0]
            probability = model.predict_proba(features_copy)[0][1]
        except Exception as pred_error:
            print(f"DEBUG: Prediction error type: {type(pred_error)}")
            print(f"DEBUG: Prediction error: {str(pred_error)}")
            import traceback
            print(f"DEBUG: Full traceback:\n{traceback.format_exc()}")
            raise
        
        return PredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            model_used=model_name
        )
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"DEBUG Error details:\n{error_details}")
        # Return full error for debugging
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}\n\nTraceback:\n{error_details}")

@app.post("/predict/batch")
async def predict_batch(inputs: List[HeartDiseaseInput]):
    """
    Batch prediction endpoint
    
    Accepts multiple inputs and returns predictions for all
    """
    try:
        feature_names = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach',
                        'exang','oldpeak','slope','ca','thal']
        results = []
        for input_data in inputs:
            # Convert input to pandas DataFrame
            features = pd.DataFrame([[
                input_data.age,
                input_data.sex,
                input_data.cp,
                input_data.trestbps,
                input_data.chol,
                input_data.fbs,
                input_data.restecg,
                input_data.thalach,
                input_data.exang,
                input_data.oldpeak,
                input_data.slope,
                input_data.ca,
                input_data.thal
            ]], columns=feature_names)
            
            # Select model
            model = model_lr if model_lr is not None else model_rf
            model_name = "logistic_regression" if model_lr is not None else "random_forest"
            
            if model is None:
                raise HTTPException(
                    status_code=503,
                    detail="No model available"
                )
            
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0][1]
            
            results.append({
                "prediction": int(prediction),
                "probability": float(probability),
                "model_used": model_name
            })
        
        return {"predictions": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

