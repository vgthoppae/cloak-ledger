# Dockerfile
FROM python:3.12-slim

# Install system deps (optional but usually handy)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        tesseract-ocr \
        poppler-utils \
        libsm6 \
        libxext6 \
        libxrender1 \
#         libtiff5 \
        libjpeg-dev \
        libpng-dev \
        zlib1g-dev \
        libglib2.0-0 \
        # CRITICAL ADDITIONS for OpenCV Runtime
        libgl1 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libglib2.0-0 \
        libfontconfig1 \
        libice6 \
        libgtk2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Cloud Run sets PORT; we just document it/run/
EXPOSE 8000

# Start MCP server
CMD ["python", "mcp_main.py"]
