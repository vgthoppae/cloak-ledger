import cv2
import json
import os
from typing import Dict


def apply_redaction(image_path: str, plan_path: str, output_path: str) -> Dict[str, str]:
  """
  Step 4: Paints black boxes over PII based on the plan.

  Returns:
      A 'Vault' dictionary mapping fake IDs to real PII for later use.
      Example: { "<ID_001>": "John Doe" }
  """

  # 1. Load Data
  img = cv2.imread(image_path)
  with open(plan_path, 'r') as f:
    redaction_boxes = json.load(f)

  vault = {}  # Local secret storage
  counter = 1

  # 2. Iterate and Paint
  for box in redaction_boxes:
    x, y, w, h = box['x'], box['y'], box['w'], box['h']
    entity_type = box['type']

    # A. Create a Mask ID (e.g., <PERSON_1>, <ACCOUNT_5>)
    # This allows the LLM to say "Cancel the subscription for <ACCOUNT_5>"
    mask_id = f"<{entity_type}_{counter}>"
    vault[mask_id] = "HIDDEN_VALUE_IN_VAULT"  # In a real app, store the real text here if you have it
    counter += 1

    # B. Draw Black Box (The Redaction)
    # (0, 0, 0) is Black. -1 means "fill the shape".
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)

    # C. (Optional) Write the Mask ID on top so the LLM can reference it
    # We write in White (255, 255, 255) so it's visible on the black box
    font_scale = 0.5
    cv2.putText(img, mask_id, (x, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 1)

  # 3. Save the Safe Image
  cv2.imwrite(output_path, img)
  print(f"Redacted image saved to: {output_path}")

  return vault


# --- Quick Test ---
# if __name__ == "__main__":
#   # Inputs
#   raw_img = "temp_images/page_001.png"
#   plan = "redaction_plan.json"
#
#   # Outputs
#   safe_img = "page_001_SAFE.png"
#
#   if os.path.exists(plan):
#     secret_vault = apply_redaction(raw_img, plan, safe_img)
#
#     # Save the Vault locally (NEVER UPLOAD THIS)
#     with open("local_vault.json", "w") as f:
#       json.dump(secret_vault, f, indent=2)
#
#     print("Vault created. KEEP THIS FILE LOCAL.")
#   else:
#     print("Plan not found. Run Step 3 first.")