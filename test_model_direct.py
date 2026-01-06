"""Test the model directly to see what format it expects"""
from joblib import load
import pandas as pd
import numpy as np

# Load model
model = load("models/best_logreg_pipeline.joblib")

# Test with DataFrame
test_data = pd.DataFrame([[
    63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1
]], columns=['age','sex','cp','trestbps','chol','fbs','restecg','thalach',
            'exang','oldpeak','slope','ca','thal'])

print("Testing with DataFrame:")
print(f"Input shape: {test_data.shape}")
print(f"Input columns: {list(test_data.columns)}")
print(f"Input dtypes:\n{test_data.dtypes}")

try:
    prediction = model.predict(test_data)
    proba = model.predict_proba(test_data)
    print(f"Success! Prediction: {prediction[0]}, Probability: {proba[0][1]:.3f}")
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()

