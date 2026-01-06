# PowerShell script for Azure deployment
# Run this script from the project root directory

Write-Host "Azure Deployment Script for Heart Disease Prediction API" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green

# Check if Azure CLI is installed
$azCli = Get-Command az -ErrorAction SilentlyContinue
if (-not $azCli) {
    Write-Host "Azure CLI is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "https://aka.ms/installazurecliwindows" -ForegroundColor Yellow
    exit 1
}

Write-Host "`nStep 1: Checking Azure login..." -ForegroundColor Cyan
$account = az account show 2>$null
if (-not $account) {
    Write-Host "Not logged in. Please login..." -ForegroundColor Yellow
    az login
}

# Get subscription info
$sub = az account show --query "{Name:name, Id:id}" -o json | ConvertFrom-Json
Write-Host "Current subscription: $($sub.Name)" -ForegroundColor Green

# Configuration
$resourceGroup = "mlops-group29-rg"
$appServicePlan = "mlops-group29-plan"
$webAppName = "mlops-group29-heart-disease-api"
$location = "eastus"

Write-Host "`nStep 2: Creating resource group..." -ForegroundColor Cyan
az group create --name $resourceGroup --location $location

Write-Host "`nStep 3: Creating App Service Plan..." -ForegroundColor Cyan
az appservice plan create `
    --name $appServicePlan `
    --resource-group $resourceGroup `
    --sku B1 `
    --is-linux

Write-Host "`nStep 4: Creating Web App..." -ForegroundColor Cyan
az webapp create `
    --resource-group $resourceGroup `
    --plan $appServicePlan `
    --name $webAppName `
    --runtime "PYTHON:3.10"

Write-Host "`nStep 5: Configuring Web App..." -ForegroundColor Cyan
az webapp config set `
    --resource-group $resourceGroup `
    --name $webAppName `
    --startup-file "gunicorn app:app --bind 0.0.0.0:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker"

az webapp config appsettings set `
    --resource-group $resourceGroup `
    --name $webAppName `
    --settings MODEL_TYPE=logreg

Write-Host "`nStep 6: Creating deployment package..." -ForegroundColor Cyan
# Create ZIP file excluding unnecessary files
# Note: PowerShell's Compress-Archive doesn't support exclusions well, so we'll include what we need
$filesToInclude = @(
    "app.py",
    "requirements.txt",
    "startup.py",
    "startup.sh",
    "models"
)
# Create temp directory for deployment
$deployDir = "deploy_temp"
if (Test-Path $deployDir) { Remove-Item $deployDir -Recurse -Force }
New-Item -ItemType Directory -Path $deployDir | Out-Null

# Copy necessary files
Copy-Item "app.py" -Destination $deployDir -Force
Copy-Item "requirements.txt" -Destination $deployDir -Force
Copy-Item "startup.py" -Destination $deployDir -Force
if (Test-Path "startup.sh") { Copy-Item "startup.sh" -Destination $deployDir -Force }
if (Test-Path "models") { Copy-Item "models" -Destination $deployDir -Recurse -Force }

# Create ZIP
Compress-Archive -Path "$deployDir\*" -DestinationPath "deploy.zip" -Force
Remove-Item $deployDir -Recurse -Force

Write-Host "`nStep 7: Deploying to Azure..." -ForegroundColor Cyan
az webapp deployment source config-zip `
    --resource-group $resourceGroup `
    --name $webAppName `
    --src deploy.zip

Write-Host "`nDeployment complete!" -ForegroundColor Green
$appUrl = az webapp show --resource-group $resourceGroup --name $webAppName --query defaultHostName -o tsv
Write-Host "`nYour API is available at: https://$appUrl" -ForegroundColor Yellow
Write-Host "API Documentation: https://$appUrl/docs" -ForegroundColor Yellow
Write-Host "Health Check: https://$appUrl/health" -ForegroundColor Yellow

Write-Host "`nTo view logs, run:" -ForegroundColor Cyan
Write-Host "az webapp log tail --resource-group $resourceGroup --name $webAppName" -ForegroundColor White

# Cleanup
Remove-Item deploy.zip -ErrorAction SilentlyContinue

