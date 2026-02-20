# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Scapy and networking
RUN apt-get update && apt-get install -y 
    libpcap-dev 
    gcc 
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend
COPY models ./models
COPY data ./data

# Set PYTHONPATH to include backend/app
ENV PYTHONPATH=/app/backend

# Command to run the application
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
