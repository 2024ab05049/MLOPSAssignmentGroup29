# Azure Deployment Guide

This guide will help you deploy the Heart Disease Prediction API to Azure App Service.

## Prerequisites

1. Azure account with active subscription
2. Azure CLI installed ([Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
3. Python 3.8+ installed locally
4. Trained model files (`.joblib` files) from your notebook

## Step 1: Prepare Model Files

1. Ensure you have the trained model files from your notebook:
   - `models/best_logreg_pipeline.joblib` or
   - `models/logreg_cv_best_pipeline.joblib` or
   - `models/best_randomforest_pipeline.joblib` or
   - `models/rf_cv_best_pipeline.joblib`

2. Place the model files in the `models/` directory in your project root.

## Step 2: Install Azure CLI (if not already installed)

```bash
# Windows (PowerShell)
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'; rm .\AzureCLI.msi

# Or download from: https://aka.ms/installazurecliwindows
```

## Step 3: Login to Azure

```bash
az login
```

## Step 4: Create Resource Group

```bash
az group create --name mlops-group29-rg --location eastus
```

## Step 5: Create App Service Plan

```bash
az appservice plan create \
  --name mlops-group29-plan \
  --resource-group mlops-group29-rg \
  --sku B1 \
  --is-linux
```

## Step 6: Create Web App

```bash
az webapp create \
  --resource-group mlops-group29-rg \
  --plan mlops-group29-plan \
  --name mlops-group29-heart-disease-api \
  --runtime "PYTHON:3.10"
```

## Step 7: Configure App Settings

```bash
# Set Python version
az webapp config set \
  --resource-group mlops-group29-rg \
  --name mlops-group29-heart-disease-api \
  --linux-fx-version "PYTHON|3.10"

# Set startup command
az webapp config set \
  --resource-group mlops-group29-rg \
  --name mlops-group29-heart-disease-api \
  --startup-file "gunicorn app:app --bind 0.0.0.0:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker"

# Optional: Set model type (logreg or randomforest)
az webapp config appsettings set \
  --resource-group mlops-group29-rg \
  --name mlops-group29-heart-disease-api \
  --settings MODEL_TYPE=logreg
```

## Step 8: Install Gunicorn (if not in requirements)

Add to `requirements.txt`:
```
gunicorn==21.2.0
```

## Step 9: Deploy the Application

### Option A: Using Azure CLI (ZIP Deploy)

```bash
# Create a deployment package
# Make sure you're in the project root directory
# Include all files: app.py, requirements.txt, models/, etc.

# Create ZIP file (Windows PowerShell)
Compress-Archive -Path * -DestinationPath deploy.zip -Force

# Deploy
az webapp deployment source config-zip \
  --resource-group mlops-group29-rg \
  --name mlops-group29-heart-disease-api \
  --src deploy.zip
```

### Option B: Using Git Deployment

```bash
# Configure local git deployment
az webapp deployment source config-local-git \
  --resource-group mlops-group29-rg \
  --name mlops-group29-heart-disease-api

# Get deployment URL
DEPLOYMENT_URL=$(az webapp deployment source show \
  --resource-group mlops-group29-rg \
  --name mlops-group29-heart-disease-api \
  --query url -o tsv)

# Add remote and push
git remote add azure $DEPLOYMENT_URL
git push azure main
```

### Option C: Using VS Code Azure Extension

1. Install the "Azure App Service" extension in VS Code
2. Right-click on your project folder
3. Select "Deploy to Web App"
4. Follow the prompts

## Step 10: Verify Deployment

1. Get your app URL:
```bash
az webapp show \
  --resource-group mlops-group29-rg \
  --name mlops-group29-heart-disease-api \
  --query defaultHostName -o tsv
```

2. Test the API:
```bash
# Health check
curl https://mlops-group29-heart-disease-api.azurewebsites.net/health

# Test prediction
curl -X POST https://mlops-group29-heart-disease-api.azurewebsites.net/predict \
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

## Step 11: View Logs

```bash
az webapp log tail \
  --resource-group mlops-group29-rg \
  --name mlops-group29-heart-disease-api
```

## Alternative: Deploy to Azure Container Apps

If you prefer containerized deployment:

1. Create a Dockerfile (see `Dockerfile` in project)
2. Build and push to Azure Container Registry
3. Deploy to Azure Container Apps

## Troubleshooting

### Model Not Found Error
- Ensure model files are in the `models/` directory
- Check file paths in Azure App Service logs
- Verify model files are included in deployment package

### Import Errors
- Check that all dependencies are in `requirements.txt`
- Verify Python version matches (3.10 recommended)

### Port Issues
- Azure App Service automatically sets the PORT environment variable
- The app uses `os.getenv("PORT", 8000)` to handle this

## API Documentation

Once deployed, visit:
- Swagger UI: `https://your-app-name.azurewebsites.net/docs`
- ReDoc: `https://your-app-name.azurewebsites.net/redoc`

## Cost Optimization

- Use Basic (B1) tier for development/testing
- Scale up to Standard tier for production
- Consider Azure Container Apps for better cost efficiency at scale

## Next Steps

1. Set up CI/CD pipeline (GitHub Actions or Azure DevOps)
2. Configure custom domain
3. Set up Application Insights for monitoring
4. Configure authentication if needed
5. Set up auto-scaling rules

