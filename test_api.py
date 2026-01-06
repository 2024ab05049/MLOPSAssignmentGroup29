"""
Test script for the Heart Disease Prediction API
Run this locally before deploying to Azure
"""
import requests
import json

# Local testing
BASE_URL = "http://localhost:8000"

# Azure deployment URL (update after deployment)
# BASE_URL = "https://mlops-group29-heart-disease-api.azurewebsites.net"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_root():
    """Test root endpoint"""
    print("Testing / endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_predict():
    """Test prediction endpoint"""
    print("Testing /predict endpoint...")
    
    # Sample input data
    sample_data = {
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
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=sample_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()

def test_batch_predict():
    """Test batch prediction endpoint"""
    print("Testing /predict/batch endpoint...")
    
    batch_data = [
        {
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
        },
        {
            "age": 37,
            "sex": 1,
            "cp": 2,
            "trestbps": 130,
            "chol": 250,
            "fbs": 0,
            "restecg": 1,
            "thalach": 187,
            "exang": 0,
            "oldpeak": 3.5,
            "slope": 0,
            "ca": 0,
            "thal": 2
        }
    ]
    
    response = requests.post(
        f"{BASE_URL}/predict/batch",
        json=batch_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("Heart Disease Prediction API - Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_health()
        test_root()
        test_predict()
        test_batch_predict()
        print("All tests completed!")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")
        print("Make sure the API is running locally (python app.py) or update BASE_URL for Azure deployment.")
    except Exception as e:
        print(f"Error: {e}")

