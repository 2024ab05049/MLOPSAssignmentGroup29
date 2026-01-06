"""Debug the pipeline to understand what it expects"""
from joblib import load
import pandas as pd
import numpy as np

# Load model
model = load("models/best_logreg_pipeline.joblib")

print("Pipeline steps:")
for name, step in model.named_steps.items():
    print(f"  {name}: {type(step).__name__}")

print("\nPreprocessor info:")
prep = model.named_steps['prep']
print(f"  Type: {type(prep)}")
print(f"  Transformers: {prep.transformers}")

# Test with exact format from training
NUMERIC_COLS = ['age','trestbps','chol','thalach','oldpeak','ca']
CATEGORICAL_COLS = ['sex','cp','fbs','restecg','exang','slope','thal']

test_data = pd.DataFrame([[
    63.0, 1, 3, 145.0, 233.0, 1, 0, 150.0, 0, 2.3, 0, 0.0, 1
]], columns=['age','sex','cp','trestbps','chol','fbs','restecg','thalach',
            'exang','oldpeak','slope','ca','thal'])

# Ensure dtypes
for c in NUMERIC_COLS:
    test_data[c] = pd.to_numeric(test_data[c], errors='coerce')
for c in CATEGORICAL_COLS:
    test_data[c] = pd.to_numeric(test_data[c], errors='coerce')

print(f"\nTest data:\n{test_data}")
print(f"\nTest data dtypes:\n{test_data.dtypes}")

# Try transforming just the preprocessor
print("\nTesting preprocessor transform...")
try:
    transformed = prep.transform(test_data)
    print(f"Transform successful! Output shape: {transformed.shape}, type: {type(transformed)}")
except Exception as e:
    print(f"Transform failed: {e}")
    import traceback
    traceback.print_exc()

# Try full prediction
print("\nTesting full prediction...")
try:
    pred = model.predict(test_data)
    proba = model.predict_proba(test_data)
    print(f"Prediction successful! Pred: {pred[0]}, Proba: {proba[0][1]:.3f}")
except Exception as e:
    print(f"Prediction failed: {e}")
    import traceback
    traceback.print_exc()

