# Heart Disease Prediction API - MLOps Assignment Group 29

This project contains a machine learning API for predicting heart disease risk, deployed on Azure.

## Project Structure

```
.
├── app.py                      # FastAPI application
├── requirements.txt            # Python dependencies
├── startup.py                 # Startup script for Azure
├── Dockerfile                 # Docker configuration
├── test_api.py                # API testing script
├── deploy-azure.ps1          # Azure deployment script (PowerShell)
├── azure-deploy.md           # Detailed deployment guide
├── models/                    # Trained model files (add your .joblib files here)
└── MLOPS_Assignment_1_Group_29.ipynb  # Original notebook
```

## Features

- RESTful API built with FastAPI
- Heart disease risk prediction using trained ML models
- Support for both Logistic Regression and Random Forest models
- Batch prediction endpoint
- Interactive API documentation (Swagger UI)
- Health check endpoint
- Ready for Azure App Service deployment

## 🚀 Quick Deployment

### Automated CI/CD (Recommended)

1. **One-time setup:**
   ```powershell
   # Create Azure resources
   .\deploy-azure.ps1
   
   # Get publish profile from Azure Portal
   # Add to GitHub Secrets as AZURE_WEBAPP_PUBLISH_PROFILE
   ```

2. **Push to GitHub:**
   ```bash
   git push origin main
   ```
   
   Deployment happens automatically! See [CICD_SETUP.md](CICD_SETUP.md) for details.

### Manual Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for quick manual deployment options.

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add model files:**
   - Place your trained model files (`.joblib`) in the `models/` directory
   - Supported model files:
     - `best_logreg_pipeline.joblib`
     - `logreg_cv_best_pipeline.joblib`
     - `best_randomforest_pipeline.joblib`
     - `rf_cv_best_pipeline.joblib`

3. **Run the API:**
   ```bash
   python app.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Test the API:**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Run test script: `python test_api.py`

### Azure Deployment

#### Option 1: Using PowerShell Script (Windows)

```powershell
.\deploy-azure.ps1
```

#### Option 2: Using Azure CLI (Manual)

See detailed instructions in [azure-deploy.md](azure-deploy.md)

#### Option 3: Using Docker

1. Build the Docker image:
   ```bash
   docker build -t heart-disease-api .
   ```

2. Run locally:
   ```bash
   docker run -p 8000:8000 heart-disease-api
   ```

3. Deploy to Azure Container Apps (see azure-deploy.md)

## API Endpoints

### `GET /`
Root endpoint - Returns API information

### `GET /health`
Health check endpoint

### `POST /predict`
Single prediction endpoint

**Request Body:**
```json
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
}
```

**Response:**
```json
{
  "prediction": 1,
  "probability": 0.85,
  "model_used": "logistic_regression"
}
```

### `POST /predict/batch`
Batch prediction endpoint - Accepts array of inputs

## Model Input Features

- `age`: Age in years
- `sex`: Sex (0=female, 1=male)
- `cp`: Chest pain type (0-3)
- `trestbps`: Resting blood pressure
- `chol`: Serum cholesterol in mg/dl
- `fbs`: Fasting blood sugar > 120 mg/dl (0=no, 1=yes)
- `restecg`: Resting electrocardiographic results (0-2)
- `thalach`: Maximum heart rate achieved
- `exang`: Exercise induced angina (0=no, 1=yes)
- `oldpeak`: ST depression induced by exercise
- `slope`: Slope of peak exercise ST segment (0-2)
- `ca`: Number of major vessels colored by flourosopy
- `thal`: Thalassemia (0-3)

## Environment Variables

- `PORT`: Server port (default: 8000)
- `MODEL_TYPE`: Model to use - "logreg" or "randomforest" (default: "logreg")

## Testing

Run the test script:
```bash
python test_api.py
```

Or use curl:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

## Troubleshooting

### Model Not Found
- Ensure model files are in the `models/` directory
- Check that model files have correct names
- Verify file paths in application logs

### Port Issues
- Azure App Service automatically sets the PORT environment variable
- For local development, use port 8000

### Import Errors
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

## Team Members

- Vikram (2024AB05100)
- R Nishanth (2024AA05994)
- Meera Hari Iyer (2024AB05097)
- Ramesh N (2024AB05049)
- Nishanth V (2024AA05920)

## License

This project is part of the MLOps Assignment for BITS WILP SEM 3 Group 29.

