# Dockerfile for Azure Container Apps deployment
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY startup.py .

# Create models directory
RUN mkdir -p models

# Copy model files (if available)
# Note: In production, you might want to download models from Azure Blob Storage
COPY models/ ./models/

# Expose port
EXPOSE 8000

# Set environment variables
ENV PORT=8000
ENV MODEL_TYPE=logreg

# Run the application
CMD ["python", "startup.py"]

