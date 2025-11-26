# Dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV SPACY_MODEL en_core_web_lg

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

# --- SPACY MODEL INSTALLATION ---
# 1. Download the specific model using spaCy's official command
RUN python -m spacy download ${SPACY_MODEL}

# 2. (Optional, but good practice) Link the downloaded model
# This makes sure spacy.load('en_core_web_lg') works correctly
RUN python -m spacy link ${SPACY_MODEL} ${SPACY_MODEL}
# ---------------------------------

# Copy code
COPY . .

# Cloud Run sets PORT; we just document it/run/
EXPOSE 8000

# Start MCP server
CMD ["python", "mcp_main.py"]
