# Setting Up Azure Credentials for GitHub Actions

To enable GitHub Actions to deploy to Azure, you need to create an Azure Service Principal and add it as a GitHub secret.

## Option 1: Using Azure CLI (Recommended)

### Step 1: Create Service Principal

Run this command in Azure CLI (replace with your subscription ID and resource group):

```bash
# Login to Azure first
az login

# Get your subscription ID
az account show --query id -o tsv

# Create service principal (replace SUBSCRIPTION_ID and RESOURCE_GROUP)
az ad sp create-for-rbac \
  --name "github-actions-mlops-group29" \
  --role contributor \
  --scopes /subscriptions/SUBSCRIPTION_ID/resourceGroups/mlops-group29-rg \
  --sdk-auth
```

**Important:** Replace:
- `SUBSCRIPTION_ID` with your actual subscription ID
- The scope can be `/subscriptions/SUBSCRIPTION_ID` for subscription-level access, or `/subscriptions/SUBSCRIPTION_ID/resourceGroups/mlops-group29-rg` for resource group level

### Step 2: Copy the Output

The command will output JSON like this:

```json
{
  "clientId": "xxxx-xxxx-xxxx-xxxx",
  "clientSecret": "xxxx-xxxx-xxxx-xxxx",
  "subscriptionId": "xxxx-xxxx-xxxx-xxxx",
  "tenantId": "xxxx-xxxx-xxxx-xxxx",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

### Step 3: Add to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `AZURE_CREDENTIALS`
5. Value: Paste the **entire JSON output** from Step 2
6. Click **Add secret**

## Option 2: Using Azure Portal

### Step 1: Create App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Name: `github-actions-mlops-group29`
5. Click **Register**
6. Note down:
   - **Application (client) ID**
   - **Directory (tenant) ID**

### Step 2: Create Client Secret

1. In your app registration, go to **Certificates & secrets**
2. Click **New client secret**
3. Add description and expiration
4. Click **Add**
5. **Copy the secret value immediately** (you won't see it again!)

### Step 3: Assign Role

1. Go to your **Subscription** or **Resource Group**
2. Click **Access control (IAM)**
3. Click **Add** → **Add role assignment**
4. Role: **Contributor**
5. Assign access to: **User, group, or service principal**
6. Select your app: `github-actions-mlops-group29`
7. Click **Save**

### Step 4: Create JSON for GitHub

Create a JSON file with this structure:

```json
{
  "clientId": "YOUR_APPLICATION_CLIENT_ID",
  "clientSecret": "YOUR_CLIENT_SECRET_VALUE",
  "subscriptionId": "YOUR_SUBSCRIPTION_ID",
  "tenantId": "YOUR_TENANT_ID",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

Replace:
- `YOUR_APPLICATION_CLIENT_ID` - from Step 1
- `YOUR_CLIENT_SECRET_VALUE` - from Step 2
- `YOUR_SUBSCRIPTION_ID` - your Azure subscription ID
- `YOUR_TENANT_ID` - from Step 1

### Step 5: Add to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `AZURE_CREDENTIALS`
5. Value: Paste the **entire JSON** from Step 4
6. Click **Add secret**

## Verify Setup

After adding the secret, your GitHub Actions workflow should be able to:
- Authenticate to Azure
- Create resource groups
- Create App Service resources
- Deploy your application

## Security Best Practices

1. **Use least privilege:** Only grant Contributor role to the specific resource group, not the entire subscription
2. **Rotate secrets:** Regularly update the client secret
3. **Use separate service principals:** Create different service principals for different environments (dev, staging, prod)
4. **Monitor usage:** Check Azure AD logs for service principal activity

## Troubleshooting

### "Authorization Failed" Error

- Ensure the service principal has Contributor role
- Verify the scope includes the resource group or subscription
- Check that the subscription ID in the JSON matches your actual subscription

### "Resource Group Not Found"

- The workflow will create it automatically if you have permissions
- Or create it manually first: `az group create --name mlops-group29-rg --location eastus`

### "Invalid Credentials"

- Verify the JSON format is correct (no extra commas, proper quotes)
- Ensure the client secret hasn't expired
- Check that all IDs match your Azure account

## Quick Command Reference

```bash
# Get subscription ID
az account show --query id -o tsv

# Get tenant ID
az account show --query tenantId -o tsv

# List service principals
az ad sp list --display-name "github-actions-mlops-group29"

# Delete service principal (if needed)
az ad sp delete --id <client-id>
```

