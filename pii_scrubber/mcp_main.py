import os, logging
import gcloud_storage
import base64

# server.py
from mcp.server.fastmcp import FastMCP

import cloak_logger, pii_driver
import logging

# Create an MCP server
mcp = FastMCP(
    "File Upload MCP Server",
    stateless_http=True,
    port=8000,
    host="0.0.0.0",
)

clog = cloak_logger.CloakLogger()
clog.configure()

BUCKET_NAME = "cloak_ledger_kaggle"  # e.g., 'gcp-public-data-landsat'
OBJECT_NAME = "invoice.png"  # e.g., 'index.html' or 'images/photo.jpg'
LOCAL_FILE_PATH = "downloaded_invoice.png"

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
    try:
        try:
            print("received file")
            gcloud_storage.download_public_gcs_object(bucket_name=BUCKET_NAME,
                                                  object_name=OBJECT_NAME,
                                                  destination_file_name=LOCAL_FILE_PATH)

            with open(LOCAL_FILE_PATH, "rb") as f:
                img_bytes = f.read()
            pd = pii_driver.PiiDriver(img_bytes= img_bytes)
            print("after constructor")
            pd.do_ocr()
            print("after ocr")
            pd.plan_redact()
            print("after plan redact")
            pd.apply_redact()
            print("after apply redact")

            redacted_object_name = "redacted_" + OBJECT_NAME
            gcloud_storage.upload_to_gcs(bucket_name=BUCKET_NAME,
                                         source_file_name="safe.png",
                                         destination_blob_name=redacted_object_name)
            logging.info("redacted file uploaded successfully")
            logging.info("redact completed successfully")
        except Exception as e:
            print(e)
        # with open("safe.png", "rb") as f:
        #     redacted_bytes = f.read()
        #
        # redacted_b64 = base64.b64encode(redacted_bytes).decode("ascii")

        # return {
        #     "mime_type": "image/png",  # or pdf, etc.
        #     "image_b64": redacted_b64,  # JSON-safe string instead of bytes
        #     "message": "Redaction completed",
        # }
        return {
            "message": "success"
        }

    except Exception as e:
        logging.error(e)
        return None

if __name__ == "__main__":
    # Streamable HTTP transport on /mcp
    mcp.run(transport="streamable-http")
