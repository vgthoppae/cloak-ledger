import pytesseract
from pytesseract import Output
import cv2
import json
import logging
from typing import List, Dict


# CONFIG: Point this to your Tesseract executable if not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_coordinates(image_path: str) -> List[Dict]:
  """
  Step 2: OCR the image to get text AND location data.

  Args:
      image_path: Path to the .png file from Step 1.

  Returns:
      List of dictionaries. Each dict represents one word:
      {
          "text": "Invoice",
          "left": 100, "top": 50, "width": 60, "height": 20,
          "conf": 90 (confidence score)
      }
  """

  # 1. Load Image
  img = cv2.imread(image_path)

  # 2. Run OCR with 'image_to_data'
  # This returns a dictionary with lists for 'left', 'top', 'text', etc.
  results = pytesseract.image_to_data(img, output_type=Output.DICT)

  coordinate_map = []

  # 3. Parse the Results
  n_boxes = len(results['text'])
  for i in range(n_boxes):
    # Filter out empty text and low-confidence noise
    text = results['text'][i].strip()
    conf = int(results['conf'][i])

    if text and conf > 30:  # Confidence threshold (0-100)
      word_data = {
        "text": text,
        "left": results['left'][i],
        "top": results['top'][i],
        "width": results['width'][i],
        "height": results['height'][i],
        "conf": conf
      }
      coordinate_map.append(word_data)

  logging.debug("Completed OCR read..")
  return coordinate_map


def save_coordinate_map(coord_map: List[Dict], output_path: str):
  """Helper to save the map as JSON for Step 3 (Presidio)"""
  with open(output_path, 'w') as f:
    json.dump(coord_map, f, indent=2)
  logging.debug(f"Saved coordinate map to {output_path}")
