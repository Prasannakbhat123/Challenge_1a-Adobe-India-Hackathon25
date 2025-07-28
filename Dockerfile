# Adobe Hackathon Round 1A - PDF Outline Extraction

FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/input /app/output

# Copy application code
COPY src/ ./src/

# Set permissions
RUN chmod +x src/main.py

# Default command - run Round 1A processor
CMD ["python3", "src/main.py"]
