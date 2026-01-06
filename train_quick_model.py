"""
Quick model training script for local testing
This trains a simple model using the same data and preprocessing as the notebook
"""
import sys
import os
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import requests
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from joblib import dump

# Create directories
BASE_DIR = Path(".")
DATA_DIR = BASE_DIR / "Data" / "raw"
MODEL_DIR = BASE_DIR / "models"
PROCESSED_DIR = BASE_DIR / "Data" / "processed"

for d in [DATA_DIR, MODEL_DIR, PROCESSED_DIR]:
    d.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Quick Model Training for Local Testing")
print("=" * 60)
print()

# Download data if not exists
DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
DATA_FILE = DATA_DIR / "processed.cleveland.data"

if not DATA_FILE.exists():
    print("Downloading dataset...")
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()
        with open(DATA_FILE, 'wb') as f:
            f.write(response.content)
        print("[OK] Dataset downloaded")
    except Exception as e:
        print(f"[ERROR] Error downloading dataset: {e}")
        sys.exit(1)
else:
    print("[OK] Dataset already exists")

# Load and preprocess data
print("\nLoading and preprocessing data...")
COLS = [
    'age','sex','cp','trestbps','chol','fbs','restecg','thalach',
    'exang','oldpeak','slope','ca','thal','num'
]
NUMERIC_COLS = ['age','trestbps','chol','thalach','oldpeak','ca']
CATEGORICAL_COLS = ['sex','cp','fbs','restecg','exang','slope','thal']
TARGET_COL = 'target'

df = pd.read_csv(DATA_FILE, header=None, names=COLS, na_values=['?','-9'])

# Binarize target
df[TARGET_COL] = (df['num'] > 0).astype(int)
df = df.drop(columns=['num'])

# Enforce numeric dtypes
for c in NUMERIC_COLS:
    df[c] = pd.to_numeric(df[c], errors='coerce')
for c in CATEGORICAL_COLS:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# Imputation
num_imputer = SimpleImputer(strategy='median')
cat_imputer = SimpleImputer(strategy='most_frequent')
df_num = pd.DataFrame(num_imputer.fit_transform(df[NUMERIC_COLS]), columns=NUMERIC_COLS)
df_cat = pd.DataFrame(cat_imputer.fit_transform(df[CATEGORICAL_COLS]), columns=CATEGORICAL_COLS)
df_clean = pd.concat([df_num, df_cat, df[TARGET_COL]], axis=1)

print(f"[OK] Data loaded: {df_clean.shape[0]} samples, {df_clean.shape[1]-1} features")
print(f"  Positive cases: {df_clean[TARGET_COL].sum()}, Negative: {(df_clean[TARGET_COL]==0).sum()}")

# Prepare features and target
X = df_clean[NUMERIC_COLS + CATEGORICAL_COLS].copy()
y = df_clean[TARGET_COL].copy()

# Build preprocessing pipeline
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_pipeline, NUMERIC_COLS),
        ('cat', categorical_pipeline, CATEGORICAL_COLS)
    ], remainder='drop'
)

# Train model
print("\nTraining Logistic Regression model...")
log_reg = LogisticRegression(solver='liblinear', class_weight='balanced',
                             random_state=42, max_iter=1000, C=0.1, penalty='l2')

pipe_lr = Pipeline([('prep', preprocessor), ('clf', log_reg)])

# Train on full dataset (for quick testing)
pipe_lr.fit(X, y)

# Evaluate
from sklearn.metrics import accuracy_score, roc_auc_score
y_pred = pipe_lr.predict(X)
y_proba = pipe_lr.predict_proba(X)[:, 1]
acc = accuracy_score(y, y_pred)
roc = roc_auc_score(y, y_proba)

print(f"[OK] Model trained")
print(f"  Training Accuracy: {acc:.3f}")
print(f"  Training ROC-AUC: {roc:.3f}")

# Save model
model_path = MODEL_DIR / "best_logreg_pipeline.joblib"
dump(pipe_lr, model_path)
print(f"\n[OK] Model saved to: {model_path}")

print("\n" + "=" * 60)
print("Training complete! You can now test the API.")
print("=" * 60)
print("\nNext steps:")
print("1. Run: python app.py")
print("2. Open: http://localhost:8000/docs")
print("3. Or test with: python test_api.py")

