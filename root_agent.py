from pii_scrubber.pdf_converter import pdf_converter_main
from pathlib import Path
import logging, os
from pii_scrubber.ocr import ocr_main
from pii_scrubber.redact import planner, painter


class RootAgent:
  def __init__(self):
    self.desc = "Root Agent"
    self.images_dir = "pii_scrubber/src_images"
    self.src_path = ""
    self.ocr_map_path = "./ocr_map.json"

  def prompt_input(self):
    self.src_path = input("Enter the full file path to the billing statement: ").strip()
    if self.src_path == "":
      self.src_path = "/Users/vgthoppae/Downloads/realistic_medical_invoice.pdf"

  def validate(self):
    if not os.path.isfile(self.src_path):
      msg = "Source file is not valid or does not exist in the given location"
      logging.error(msg)
      raise Exception(msg)
    return True

  def convert_to_image(self):
    self.validate()

    return pdf_converter_main.convert_pdf_to_images(
      pdf_path = self.src_path,
      output_folder = self.images_dir)

  def do_ocr(self):
    self.validate()

    images_dir = Path(self.images_dir)
    result_list = []
    for png_file in images_dir.glob("*.png"):
      logging.info(f"Extracting {png_file.name}")
      result = ocr_main.extract_text_coordinates(png_file)
      result_list.extend(result)

    ocr_main.save_coordinate_map(result_list, self.ocr_map_path)

  def plan_redact(self):
    self.validate()

    redaction_boxes = planner.analyze_and_map(self.ocr_map_path)
    planner.save_redact_plan(redaction_boxes)

  def apply_redact(self):
    self.validate()

    painter.apply_redaction(self.images_dir + "/realistic_medical_invoice.pdf_page_001.png",
                            plan_path="./redaction_plan.json", output_path="pii_scrubber/vault/safe.png")





