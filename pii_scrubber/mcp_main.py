import os

# server.py
from mcp.server.fastmcp import FastMCP

from pii_scrubber import cloak_logger, pii_driver
import logging

# Create an MCP server
mcp = FastMCP(
    "File Upload MCP Server",
    json_response=True,
    stateless_http=True,
    port=8000,
    host="0.0.0.0",
)

clog = cloak_logger.CloakLogger()
clog.configure()

# A simple tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# -------------------------------------------------------
# TOOL: Accepts a file upload (binary) + optional metadata
# -------------------------------------------------------
@mcp.tool()
def process_file(file_bytes: bytes, filename: str = "uploaded_file") -> dict:
    """
    Process an uploaded file.
    - `file_bytes`: raw bytes of uploaded file (PDF, PNG, TXT, CSV, etc.)
    - `filename`: optional client-supplied filename

    This is where your business logic goes.
    """

    pd = pii_driver.PiiDriver(img_bytes= file_bytes)
    pd.do_ocr()
    pd.plan_redact()
    pd.apply_redact()

    with open("safe.png", "rb") as f:
        return f.read()

if __name__ == "__main__":
    # Cloud Run sets PORT in the environment
    # port = int(os.environ.get("PORT", "8000"))

    # os.environ["MCP_TRANSPORT"] = "streamable-http"
    # os.environ["MCP_HOST"] = "0.0.0.0"
    # os.environ["MCP_PORT"] = "8080"
    # os.environ["MCP_HTTP_PATH"] = "/mcp"

    # Streamable HTTP transport on /mcp
    mcp.run(transport="streamable-http")
