import os, io
from pdf2image import convert_from_path, convert_from_bytes
from typing import List, Tuple


def convert_pdf_to_images(pdf_path: str, pdf_bytes: bytes, poppler_path: str = None) -> List[str]:
  """
  Step 1: Convert PDF pages to high-quality images for OCR/Redaction.

  Args:
      pdf_path: Path to the input PDF.
      pdf_bytes: PDF Content in bytes.
      poppler_path: (Optional) Path to the poppler/bin directory for Windows/Mac troubleshooting.

  Returns:
      List of tuples: [(image_data_bytes, mime_type), ...]
  """

  # 1. Create output directory if it doesn't exist
  # os.makedirs(output_folder, exist_ok=True)

  # print(f"Converting '{pdf_path}' to images...")

  # 2. Convert to images
  # dpi=300 is CRITICAL. Lower DPI (like 72) will cause OCR failures on small text.
  # fmt='png' is lossless, preventing compression artifacts from ruining text.
  try:
    if pdf_path:
      images = convert_from_path(
        pdf_path,
        dpi=300,
        fmt='png',
        thread_count=4  # Speeds up conversion
      )
    elif pdf_bytes:
      images = convert_from_bytes(
        pdf_file= pdf_bytes,
        dpi=300,
        fmt='png',
        thread_count=4  # Speeds up conversion
      )
    else:
      raise Exception("no pdf file path or bytes content provided")
  except Exception as e:
    print(f"Error during conversion. Is Poppler installed? \n{e}")
    return []

  # 3. Extract file name
  # file_name = os.path.basename(pdf_path)

  image_data_list = []

  # 4. Save pages as individual image files
  for i, image in enumerate(images):
    # Use a BytesIO buffer to store the image data in memory
    byte_arr = io.BytesIO()

    # Save the image data (PNG format for lossless quality) to the buffer
    # This is equivalent to image.save(filename, 'PNG') but in memory
    image.save(byte_arr, format='PNG')

    # Get the raw bytes from the buffer
    image_bytes = byte_arr.getvalue()

    # Store the bytes and the MIME type for easy API transport
    image_data_list.append((image_bytes, "image/png"))

    print(f"Processed page {i + 1} into {len(image_bytes)} bytes.")

  return image_data_list
