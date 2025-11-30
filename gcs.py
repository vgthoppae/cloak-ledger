from google.cloud import storage
import io

BUCKET_NAME = "cloak_ledger_kaggle"


def upload_bytes_to_gcs(data_bytes, destination_blob_name):
  """
  Uploads bytes data directly to a Google Cloud Storage object.

  Args:
      data_bytes (bytes): The raw bytes object to upload.
      destination_blob_name (str): The desired path/name of the object in the bucket.
  """

  # Instantiate the client (assumes credentials are set up)
  storage_client = storage.Client(project="kaggle-ai-agent-478218")

  # Get the target bucket and blob (object)
  bucket = storage_client.bucket(BUCKET_NAME)
  blob = bucket.blob(destination_blob_name)

  print(f"Uploading {len(data_bytes)} bytes to gs://{BUCKET_NAME}/{destination_blob_name}...")

  blob.upload_from_string(
    data=data_bytes,
    content_type="image/png"
  )

  print(f"✅ Upload successful. Data saved as object: {destination_blob_name}")
  print(f"   Content Type set to: {blob.content_type}")