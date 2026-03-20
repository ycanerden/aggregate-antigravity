FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the Chromium browser matches the pip playwright version
RUN playwright install chromium

# Copy backend source code
COPY . .

# Run FastAPI using dynamic PORT fallback
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
