import os
from pdf2image import convert_from_path
from typing import List


def convert_pdf_to_images(pdf_path: str, output_folder: str = "temp_images") -> List[str]:
  """
  Step 1: Convert PDF pages to high-quality images for OCR/Redaction.

  Args:
      pdf_path: Path to the input PDF.
      output_folder: Where to save the temporary images.

  Returns:
      List of file paths to the generated images.
  """

  # 1. Create output directory if it doesn't exist
  os.makedirs(output_folder, exist_ok=True)

  print(f"Converting '{pdf_path}' to images...")

  # 2. Convert to images
  # dpi=300 is CRITICAL. Lower DPI (like 72) will cause OCR failures on small text.
  # fmt='png' is lossless, preventing compression artifacts from ruining text.
  try:
    images = convert_from_path(
      pdf_path,
      dpi=300,
      fmt='png',
      thread_count=4  # Speeds up conversion
    )
  except Exception as e:
    print(f"Error during conversion. Is Poppler installed? \n{e}")
    return []

  image_paths = []

  # 3. Extract file name
  file_name = os.path.basename(pdf_path)

  # 4. Save pages as individual image files
  for i, image in enumerate(images):
    # Naming convention: page_001.png, page_002.png
    image_name = f"{file_name}_page_{i + 1:03d}.png"
    full_path = os.path.join(output_folder, image_name)

    image.save(full_path, "PNG")
    image_paths.append(full_path)
    print(f"Saved: {full_path}")

  return image_paths
