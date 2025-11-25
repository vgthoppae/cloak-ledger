import json
from typing import List, Dict, Tuple
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern, RecognizerResult


def analyze_and_map(ocr_map_path: str) -> List[Dict]:
  """
  Step 3: Analyze text for PII and map it back to pixel coordinates.

  Args:
      ocr_map_path: Path to the JSON map from Step 2.

  Returns:
      List of bounding boxes to redact: [{'x': 10, 'y': 10, 'w': 50, 'h': 20, 'type': 'PERSON'}, ...]
  """

  # 1. Load the OCR Map
  with open(ocr_map_path, 'r') as f:
    ocr_words = json.load(f)

  # 2. Reconstruct Full Text (Presidio needs context!)
  # We rebuild the sentence so Presidio sees "John Doe", not "John", "Doe" separately.
  full_text = ""
  word_index_map = []  # Maps character indices to original word objects

  current_char_idx = 0
  for word_obj in ocr_words:
    text = word_obj['text']
    # We assume a space between words for reconstruction
    # (This is a simplification; perfect reconstruction requires 'left' diffs)
    full_text += text + " "

    # Store the start/end char index for this specific word
    end_char_idx = current_char_idx + len(text)
    word_obj['start_char'] = current_char_idx
    word_obj['end_char'] = end_char_idx

    word_index_map.append(word_obj)
    current_char_idx = end_char_idx + 1  # +1 for the space we added

  print(f"Reconstructed Text: {full_text[:50]}...")

  # 3. Configure Presidio
  analyzer = AnalyzerEngine()

  # Optional: Add a custom recognizer for "Account Numbers" if they aren't standard
  # This is useful for specific bank formats
  account_pattern = Pattern(name="bank_account_custom", regex=r"\b\d{8,12}\b", score=0.5)
  account_recognizer = PatternRecognizer(supported_entity="BANK_ACCT_CUSTOM", patterns=[account_pattern])
  analyzer.registry.add_recognizer(account_recognizer)

  taxid_pattern = Pattern(name="tax_id_custom", regex=r"\b(\d{2}[-]\d{7})\b", score=0.5)
  taxid_recognizer = PatternRecognizer(supported_entity="TAX_ID", patterns=[taxid_pattern])
  analyzer.registry.add_recognizer(taxid_recognizer)

  routingnum_pattern = Pattern(name="routing_num_custom", regex=r"\b\d{9}\b", score=0.5)
  routingnum_recognizer = PatternRecognizer(supported_entity="ROUTING_NUM", patterns=[routingnum_pattern])
  analyzer.registry.add_recognizer(routingnum_recognizer)

  # 4. Run Analysis
  # We look for standard PII + our custom bank account pattern
  results = analyzer.analyze(
    text=full_text,
    entities=["PERSON", "US_SSN", "IBAN_CODE", "PHONE_NUMBER", "BANK_ACCT_CUSTOM", "DATE_TIME", "TAX_ID", "ROUTING_NUM"],
    language='en'
  )

  redaction_boxes = []

  # 5. The BRIDGE: Map Presidio Results (Char Indices) -> OCR Boxes (Pixels)
  for result in results:
    # result.start and result.end are character indices in 'full_text'
    print(f"Found {result.entity_type} at chars {result.start}-{result.end}")

    # Find all words that fall inside this character range
    for word_obj in word_index_map:
      # Check overlap logic
      # If the word starts before the PII ends AND ends after the PII starts
      if word_obj['start_char'] < result.end and word_obj['end_char'] > result.start:
        redaction_boxes.append({
          "x": word_obj['left'],
          "y": word_obj['top'],
          "w": word_obj['width'],
          "h": word_obj['height'],
          "type": result.entity_type,
          "label": f"<{result.entity_type}>"  # Label for re-hydration later
        })

  return redaction_boxes

# Save the plan
def save_redact_plan(redaction_boxes):
    with open("redaction_plan.json", "w") as f:
      json.dump(redaction_boxes, f, indent=2)
#
    print(f"Found {len(redaction_boxes)} items to redact. Saved to redaction_plan.json")

# # --- Quick Test ---
# if __name__ == "__main__":
#   # Test using the map we made in Step 2
#   map_file = "page_001_map.json"
#
#   try:
#     boxes = analyze_and_map(map_file)
#
#     # Save the plan
#     with open("redaction_plan.json", "w") as f:
#       json.dump(boxes, f, indent=2)
#
#     print(f"Found {len(boxes)} items to redact. Saved to redaction_plan.json")
#
#   except FileNotFoundError:
#     print("Run Step 2 first to generate the JSON map!")