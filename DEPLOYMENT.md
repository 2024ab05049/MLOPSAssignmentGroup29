# Deployment Guide - Quick Start

This is a quick reference guide for deploying the Heart Disease Prediction API to Azure.

## Quick Deployment Options

### Option 1: GitHub Actions (Recommended - Automated CI/CD)

1. **Set up Azure resources:**
   ```powershell
   .\deploy-azure.ps1
   ```

2. **Get publish profile:**
   - Azure Portal → App Service → Get publish profile
   - Or: `az webapp deployment list-publishing-profiles --resource-group mlops-group29-rg --name mlops-group29-heart-disease-api --xml`

3. **Add to GitHub Secrets:**
   - Repository → Settings → Secrets → Actions
   - Add: `AZURE_WEBAPP_PUBLISH_PROFILE` (paste XML content)

4. **Push to GitHub:**
   ```bash
   git push origin main
   ```

5. **Deployment happens automatically!**

See [CICD_SETUP.md](CICD_SETUP.md) for detailed instructions.

### Option 2: Manual Deployment (Azure CLI)

```bash
# Login
az login

# Deploy
az webapp deployment source config-zip \
    --resource-group mlops-group29-rg \
    --name mlops-group29-heart-disease-api \
    --src deploy.zip
```

### Option 3: Azure Portal

1. Go to Azure Portal
2. Navigate to your App Service
3. Go to **Deployment Center**
4. Choose **Local Git** or **GitHub**
5. Follow the setup wizard

## Verify Deployment

```bash
# Health check
curl https://mlops-group29-heart-disease-api.azurewebsites.net/health

# API docs
# Visit: https://mlops-group29-heart-disease-api.azurewebsites.net/docs
```

## View Logs

```bash
az webapp log tail \
    --resource-group mlops-group29-rg \
    --name mlops-group29-heart-disease-api
```

## Update Deployment

### With CI/CD (Recommended)
Just push to `main` branch - deployment happens automatically.

### Manual Update
```bash
# Create new deployment package
zip -r deploy.zip . -x "*.git*" "*.ipynb" "*__pycache__*"

# Deploy
az webapp deployment source config-zip \
    --resource-group mlops-group29-rg \
    --name mlops-group29-heart-disease-api \
    --src deploy.zip
```

## Troubleshooting

- **App not starting:** Check logs and startup command
- **Model not found:** Ensure model files are in deployment package
- **Import errors:** Check requirements.txt is included
- **Port issues:** Verify PORT environment variable is set

For detailed troubleshooting, see [azure-deploy.md](azure-deploy.md).

