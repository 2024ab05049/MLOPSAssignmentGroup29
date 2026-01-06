# CI/CD Pipeline Setup Guide

This guide explains how to set up continuous integration and deployment (CI/CD) for the Heart Disease Prediction API using GitHub Actions and Azure App Service.

## Overview

The project includes two GitHub Actions workflows:

1. **CI Pipeline** (`.github/workflows/ci.yml`)
   - Runs on pull requests and feature branches
   - Tests code quality, imports, and API structure
   - Does not deploy

2. **Deployment Pipeline** (`.github/workflows/azure-deploy.yml`)
   - Runs on pushes to `main`/`master` branches
   - Builds, tests, and deploys to Azure App Service
   - Includes health checks after deployment

## Prerequisites

1. **GitHub Repository**
   - Your code must be in a GitHub repository
   - Repository should have `main` or `master` as the default branch

2. **Azure Account**
   - Active Azure subscription
   - Azure App Service created (or we'll create it)

3. **Azure CLI** (for initial setup)
   - Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

## Step 1: Create Azure Resources

### Option A: Using PowerShell Script (Windows)

```powershell
.\deploy-azure.ps1
```

### Option B: Using Bash Script (Linux/Mac)

```bash
chmod +x .azure/deploy.sh
./.azure/deploy.sh
```

### Option C: Manual Azure CLI Commands

```bash
# Login to Azure
az login

# Create resource group
az group create --name mlops-group29-rg --location eastus

# Create App Service Plan
az appservice plan create \
    --name mlops-group29-plan \
    --resource-group mlops-group29-rg \
    --sku B1 \
    --is-linux

# Create Web App
az webapp create \
    --resource-group mlops-group29-rg \
    --plan mlops-group29-plan \
    --name mlops-group29-heart-disease-api \
    --runtime "PYTHON|3.10"

# Configure startup command
az webapp config set \
    --resource-group mlops-group29-rg \
    --name mlops-group29-heart-disease-api \
    --startup-file "gunicorn app:app --bind 0.0.0.0:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker"

# Set app settings
az webapp config appsettings set \
    --resource-group mlops-group29-rg \
    --name mlops-group29-heart-disease-api \
    --settings MODEL_TYPE=logreg PORT=8000
```

## Step 2: Get Azure Publish Profile

The publish profile is required for GitHub Actions to deploy to Azure.

### Method 1: Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your App Service: `mlops-group29-heart-disease-api`
3. Click on **Get publish profile** (in the Overview section)
4. Save the downloaded file (it's an XML file)

### Method 2: Azure CLI

```bash
az webapp deployment list-publishing-profiles \
    --resource-group mlops-group29-rg \
    --name mlops-group29-heart-disease-api \
    --xml > publish-profile.xml
```

## Step 3: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secret:

   **Name:** `AZURE_WEBAPP_PUBLISH_PROFILE`
   
   **Value:** Copy the entire contents of the `publish-profile.xml` file you downloaded

5. Click **Add secret**

## Step 4: Push Code to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit with CI/CD setup"

# Add remote (replace with your repository URL)
git remote add origin https://github.com/yourusername/your-repo-name.git

# Push to main branch
git branch -M main
git push -u origin main
```

## Step 5: Verify CI/CD Pipeline

### Check CI Pipeline

1. Go to your GitHub repository
2. Click on **Actions** tab
3. You should see the CI pipeline running on your push
4. Wait for it to complete - it should show green checkmarks

### Trigger Deployment

The deployment pipeline runs automatically when you push to `main` or `master`. To trigger it:

```bash
# Make a small change
echo "# Test" >> README.md
git add README.md
git commit -m "Trigger deployment"
git push
```

Or use the manual trigger:
1. Go to **Actions** tab
2. Select **Deploy to Azure App Service** workflow
3. Click **Run workflow**
4. Select branch and environment
5. Click **Run workflow**

## Step 6: Verify Deployment

After deployment completes:

1. **Check the workflow logs:**
   - Go to Actions → Latest workflow run
   - Check for any errors

2. **Test the API:**
   ```bash
   # Health check
   curl https://mlops-group29-heart-disease-api.azurewebsites.net/health
   
   # API docs
   # Visit: https://mlops-group29-heart-disease-api.azurewebsites.net/docs
   ```

3. **View logs:**
   ```bash
   az webapp log tail \
       --resource-group mlops-group29-rg \
       --name mlops-group29-heart-disease-api
   ```

## Workflow Details

### CI Pipeline (ci.yml)

**Triggers:**
- Pull requests to `main`/`master`
- Pushes to `develop` or `feature/*` branches

**Steps:**
1. Checkout code
2. Set up Python 3.10
3. Install dependencies
4. Lint code (flake8)
5. Test imports
6. Test API structure
7. Check model files (if present)

### Deployment Pipeline (azure-deploy.yml)

**Triggers:**
- Pushes to `main`/`master` branches
- Manual workflow dispatch

**Steps:**
1. Checkout code
2. Set up Python 3.10
3. Install dependencies
4. Lint code
5. Test API structure
6. Check for model files
7. Create deployment package
8. Deploy to Azure
9. Verify deployment
10. Health check

## Customization

### Change App Name

1. Update `.github/workflows/azure-deploy.yml`:
   ```yaml
   env:
     AZURE_WEBAPP_NAME: your-new-app-name
   ```

2. Update Azure resources to match

### Change Deployment Branch

Edit `.github/workflows/azure-deploy.yml`:
```yaml
on:
  push:
    branches:
      - your-branch-name
```

### Add Environment Variables

1. In Azure Portal or CLI, add app settings
2. Or update the workflow to set them during deployment

## Troubleshooting

### Deployment Fails

1. **Check GitHub Secrets:**
   - Ensure `AZURE_WEBAPP_PUBLISH_PROFILE` is set correctly
   - The XML content should be the entire file content

2. **Check Azure Resources:**
   - Verify App Service exists
   - Check resource group name matches

3. **Check Workflow Logs:**
   - Go to Actions → Failed workflow → View logs
   - Look for specific error messages

### App Not Starting

1. **Check App Service Logs:**
   ```bash
   az webapp log tail --resource-group mlops-group29-rg --name mlops-group29-heart-disease-api
   ```

2. **Verify Startup Command:**
   - Should be: `gunicorn app:app --bind 0.0.0.0:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker`

3. **Check App Settings:**
   - `PORT=8000`
   - `MODEL_TYPE=logreg`

### Model Files Missing

- Ensure model files are committed to the repository
- Or upload them manually via Azure Portal → App Service → Advanced Tools → Kudu

## Best Practices

1. **Never commit secrets** - Use GitHub Secrets
2. **Test locally first** - Run `python app.py` before deploying
3. **Monitor deployments** - Check logs after each deployment
4. **Use feature branches** - Test changes before merging to main
5. **Review CI results** - Fix linting and test issues before deploying

## Next Steps

- Set up monitoring with Application Insights
- Configure custom domain
- Set up staging environment
- Add automated testing
- Configure auto-scaling rules

