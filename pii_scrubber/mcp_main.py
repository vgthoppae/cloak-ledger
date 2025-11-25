import os

# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(
    "File Upload MCP Server",
    json_response=True,
    stateless_http=True,
    port=8000
)

# A simple tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# A simple resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# A simple prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    return f"Write a {style} greeting for someone named {name}."

# -------------------------------------------------------
# TOOL: Accepts a file upload (binary) + optional metadata
# -------------------------------------------------------
@mcp.tool()
def process_file(file: bytes, filename: str = "uploaded_file") -> dict:
    """
    Process an uploaded file.
    - `file`: raw bytes of uploaded file (PDF, PNG, TXT, CSV, etc.)
    - `filename`: optional client-supplied filename

    This is where your business logic goes.
    """

    # Example business logic: inspect file size & first bytes
    file_size = len(file)

    # Preview first 100 bytes (safe for binary)
    preview = file[:100].hex()  # hex preview for safety

    return {
        "filename": filename,
        "size_bytes": file_size,
        "hex_preview_first_100_bytes": preview,
        "message": "File processed successfully",
    }

if __name__ == "__main__":
    # Cloud Run sets PORT in the environment
    # port = int(os.environ.get("PORT", "8000"))

    # os.environ["MCP_TRANSPORT"] = "streamable-http"
    # os.environ["MCP_HOST"] = "0.0.0.0"
    # os.environ["MCP_PORT"] = "8080"
    # os.environ["MCP_HTTP_PATH"] = "/mcp"

    # Streamable HTTP transport on /mcp
    mcp.run(transport="streamable-http")
