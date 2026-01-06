# 🚀 Quick Start: Deploy to Azure with CI/CD

Follow these steps to deploy your Heart Disease Prediction API to Azure with automated CI/CD.

## Prerequisites Checklist

- [ ] Azure account with active subscription
- [ ] GitHub account
- [ ] Code pushed to GitHub repository
- [ ] Azure CLI installed (for initial setup)

## Step-by-Step Deployment

### Step 1: Create Azure Resources (One-time setup)

**Windows (PowerShell):**
```powershell
.\deploy-azure.ps1
```

**Linux/Mac (Bash):**
```bash
chmod +x .azure/deploy.sh
./.azure/deploy.sh
```

**Or manually:**
```bash
az login
az group create --name mlops-group29-rg --location eastus
az appservice plan create --name mlops-group29-plan --resource-group mlops-group29-rg --sku B1 --is-linux
az webapp create --resource-group mlops-group29-rg --plan mlops-group29-plan --name mlops-group29-heart-disease-api --runtime "PYTHON|3.10"
az webapp config set --resource-group mlops-group29-rg --name mlops-group29-heart-disease-api --startup-file "gunicorn app:app --bind 0.0.0.0:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker"
```

### Step 2: Get Azure Publish Profile

**Option A: Azure Portal**
1. Go to https://portal.azure.com
2. Navigate to: App Services → `mlops-group29-heart-disease-api`
3. Click **Get publish profile** button
4. Save the downloaded `.PublishSettings` file

**Option B: Azure CLI**
```bash
az webapp deployment list-publishing-profiles \
    --resource-group mlops-group29-rg \
    --name mlops-group29-heart-disease-api \
    --xml > publish-profile.xml
```

### Step 3: Add GitHub Secret

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
5. Value: Open the `.PublishSettings` or `publish-profile.xml` file and copy **ALL** its contents
6. Click **Add secret**

### Step 4: Push to GitHub

```bash
# If not already a git repository
git init
git add .
git commit -m "Initial commit with CI/CD"

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Step 5: Watch the Magic! ✨

1. Go to your GitHub repository
2. Click the **Actions** tab
3. You'll see the deployment workflow running
4. Wait 2-3 minutes for deployment to complete
5. Check the workflow - it should show green checkmarks ✅

### Step 6: Test Your API

Once deployment completes:

**Health Check:**
```bash
curl https://mlops-group29-heart-disease-api.azurewebsites.net/health
```

**API Documentation:**
Open in browser: `https://mlops-group29-heart-disease-api.azurewebsites.net/docs`

**Test Prediction:**
```bash
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

## 🎉 You're Done!

Your API is now:
- ✅ Deployed to Azure
- ✅ Automatically deployed on every push to `main`
- ✅ Tested before deployment
- ✅ Monitored and logged

## Future Updates

Simply push to `main` branch - deployment happens automatically!

```bash
git add .
git commit -m "Update API"
git push origin main
```

## Troubleshooting

**Deployment fails?**
- Check GitHub Actions logs for errors
- Verify `AZURE_WEBAPP_PUBLISH_PROFILE` secret is correct
- Ensure Azure resources exist

**API not working?**
- Check Azure App Service logs: `az webapp log tail --resource-group mlops-group29-rg --name mlops-group29-heart-disease-api`
- Verify model files are in the repository
- Check app settings in Azure Portal

**Need help?**
- See [CICD_SETUP.md](CICD_SETUP.md) for detailed guide
- See [azure-deploy.md](azure-deploy.md) for troubleshooting

## What's Included

- ✅ Automated CI/CD pipeline (GitHub Actions)
- ✅ Code quality checks
- ✅ Automated testing
- ✅ Health checks after deployment
- ✅ Deployment verification

## Next Steps

- Set up custom domain
- Configure Application Insights for monitoring
- Set up staging environment
- Add more comprehensive tests

