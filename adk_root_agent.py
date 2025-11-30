# %%writefile root_cloaker_agent / agent.py
#
# from google.adk.agents.llm_agent import LlmAgent
# from google.adk.models.google_llm import Gemini
# from google.adk.runners import Runner
# from pdf2image import convert_from_path
# from google.cloud import storage
# from google.genai import types
# from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams
# import io
#
# PII_MCP_URL = "https://cloak-ledger-22400194016.us-east1.run.app/mcp"  # <- include /mcp
#
# BUCKET_NAME = "cloak_ledger_kaggle"
#
# retry_config = types.HttpRetryOptions(
#   attempts=5,  # Maximum retry attempts
#   exp_base=7,  # Delay multiplier
#   initial_delay=1,
#   http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
# )
#
#
# def upload_bytes_to_gcs(data_bytes, destination_blob_name):
#   """
#   Uploads bytes data directly to a Google Cloud Storage object.
#
#   Args:
#       data_bytes (bytes): The raw bytes object to upload.
#       destination_blob_name (str): The desired path/name of the object in the bucket.
#   """
#
#   # Instantiate the client (assumes credentials are set up)
#   storage_client = storage.Client(project="kaggle-ai-agent-478218")
#
#   # Get the target bucket and blob (object)
#   bucket = storage_client.bucket(BUCKET_NAME)
#   blob = bucket.blob(destination_blob_name)
#
#   print(f"Uploading {len(data_bytes)} bytes to gs://{BUCKET_NAME}/{destination_blob_name}...")
#
#   blob.upload_from_string(
#     data=data_bytes,
#     content_type="image/png"
#   )
#
#   print(f"✅ Upload successful. Data saved as object: {destination_blob_name}")
#   print(f"   Content Type set to: {blob.content_type}")
#
#
# def pdf_to_image(pdf_path: str, page: int = 0) -> dict:
#   """
#   Convert a PDF page to a PNG image and return the image as bytes.
#
#   Args:
#       pdf_path: Path to the PDF file within the notebook environment.
#       page:     Zero-based index of the page to convert (0 = first page).
#
#   Returns:
#       {
#         "filename": "input_page_<n>.png"
#       }
#   """
#   # pdf2image uses 1-based page numbers
#   page_number = page + 1
#
#   images = convert_from_path(
#     pdf_path,
#     first_page=page_number,
#     last_page=page_number,
#   )
#
#   if not images:
#     raise ValueError(f"No page {page} found in {pdf_path}")
#
#   img = images[0]
#
#   buf = io.BytesIO()
#   img.save(buf, format="PNG")
#   img_bytes = buf.getvalue()
#
#   filename = f"{pdf_path.rsplit('/', 1)[-1].rsplit('.', 1)[0]}_page_{page}.png"
#
#   upload_bytes_to_gcs(img_bytes, filename)
#
#   return {
#     "filename": filename,
#   }
#
#
# pii_toolset = McpToolset(
#   connection_params=StreamableHTTPConnectionParams(
#     url=PII_MCP_URL,
#     # headers={"Authorization": "Bearer ..."}  # if you later secure Cloud Run
#   ),
#   tool_filter=["process_file"]
# )
#
# SYSTEM_INSTRUCTIONS = """
# You are a PII redaction orchestrator.
# When the user asks you to redact a document with a file name, you MUST:
# 1. First call the `pdf_to_image` MCP tool with that file name to convert the pdf to image
# 2. Take the returned file name from the previous step and call the 'process_file' MCP tool
# 2. Report success or failure when the tool call returns
# Do NOT guess or do anything else; always defer to the MCP tools.
# """
# # SYSTEM_INSTRUCTIONS = """
# # You are a PDF to PNG converter.
# # When the user gives you a file name, you MUST:
# # 1. Call the `pdf_to_image` MCP tool with that file name
# # 2. Report success or failure when the tool call returns
# # Do NOT guess or do anything else; always defer to the MCP tool.
# # """
#
# root_agent = LlmAgent(
#   model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
#   name="root_cloaker_agent",
#   instruction=SYSTEM_INSTRUCTIONS,
#   tools=[pdf_to_image, pii_toolset],  # <- your MCP tools live here
# )