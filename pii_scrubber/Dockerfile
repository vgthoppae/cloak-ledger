# Dockerfile
FROM python:3.12-slim

# Install system deps (optional but usually handy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

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
