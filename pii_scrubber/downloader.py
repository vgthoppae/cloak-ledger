import requests
import os


def download_public_gcs_object(bucket_name, object_name, destination_file_name):
  """Downloads a publicly accessible GCS object using its HTTP URL."""

  # 1. Construct the public HTTP URL
  gcs_url = f"https://storage.googleapis.com/{bucket_name}/{object_name}"

  print(f"Attempting to download {gcs_url}...")

  try:
    # 2. Use requests.get() to fetch the file content
    response = requests.get(gcs_url, stream=True)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    # 3. Write the content to the local file
    with open(destination_file_name, 'wb') as f:
      for chunk in response.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive new chunks
          f.write(chunk)

    print(f"✅ Download successful. File saved to: **{os.path.abspath(destination_file_name)}**")

  except requests.exceptions.RequestException as e:
    print(f"❌ An error occurred during download: {e}")
    print(
      "Please check if the bucket and object names are correct, and ensure the object is genuinely set to public (allUsers with Storage Object Viewer role).")


# --- Configuration ---
# BUCKET_NAME = "cloak_ledger_kaggle"  # e.g., 'gcp-public-data-landsat'
# OBJECT_NAME = "invoice.png"  # e.g., 'index.html' or 'images/photo.jpg'
# LOCAL_FILE_PATH = "downloaded_invoice.png"  # The name you want to save the file as locally
# --- Run the function ---
# download_public_gcs_object(BUCKET_NAME, OBJECT_NAME, LOCAL_FILE_PATH)