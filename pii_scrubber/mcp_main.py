import os, logging
import gcloud_storage
import glob

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
# OBJECT_NAME = "invoice.png"  # e.g., 'index.html' or 'images/photo.jpg'
# LOCAL_FILE_PATH = "downloaded_invoice.png"

# A simple tool for test
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# -------------------------------------------------------------
# TOOL: Accepts a file name to download from storage and redact
# -------------------------------------------------------------
@mcp.tool()
def process_file(file_name: str) -> dict:
    """
    Process an uploaded file.
    - `file_name`: client-supplied filename
    """
    try:
        try:
            print("received file")
            gcloud_storage.download_public_gcs_object(bucket_name=BUCKET_NAME,
                                                  object_name=file_name,
                                                  destination_file_name=file_name)

            with open(file_name, "rb") as f:
                img_bytes = f.read()
            pd = pii_driver.PiiDriver(file_name, img_bytes= img_bytes)
            pd.do_ocr()
            pd.plan_redact()
            pd.apply_redact()

            redacted_object_name = "redacted_" + file_name
            gcloud_storage.upload_to_gcs(bucket_name=BUCKET_NAME,
                                         source_file_name="safe.png",
                                         destination_blob_name=redacted_object_name)
            logging.info("redacted file uploaded successfully")
            logging.info("redact completed successfully")
        except Exception as e:
            print(e)

        return {
            "message": "success"
        }

    except Exception as e:
        logging.error(e)
        return None
    finally:
        cleanup()

def cleanup():
    extensions = ["*.png", "*.json"]
    for ext in extensions:
        for file_path in glob.glob(f"*{ext}"):
            os.remove(file_path)

if __name__ == "__main__":
    # Streamable HTTP transport on /mcp
    mcp.run(transport="streamable-http")
    # process_file("invoice.png")
