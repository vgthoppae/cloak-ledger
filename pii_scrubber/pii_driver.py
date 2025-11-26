from pdf_converter import pdf_converter_main
from pathlib import Path
import logging, os
from ocr import ocr_main
from redact import planner, painter


class PiiDriver:
  def __init__(self, filename, src_content= None, img_bytes=None):
    self.desc = "Root Agent"
    self.images_dir = "src_images"
    self.src_path = ""
    self.src_content = src_content
    self.ocr_map_path = "ocr_map.json"
    self.img_bytes = img_bytes
    self.file_name = filename

  def prompt_input(self):
    self.src_path = input("Enter the full file path to the billing statement: ").strip()
    if self.src_path == "":
      self.src_path = "/Users/vgthoppae/Downloads/realistic_medical_invoice.pdf"

  def validate(self):
    if not os.path.isfile(self.src_path) and not self.src_content:
      msg = "Source file is not valid or does not exist in the given location"
      logging.error(msg)
      raise Exception(msg)
    return True

  def convert_to_image(self):
    self.validate()

    return pdf_converter_main.convert_pdf_to_images(
      pdf_path  = self.src_path,
      pdf_bytes = self.src_content)

  def do_ocr(self):
    # self.validate()

    images_dir = Path(self.images_dir)
    # result_list = []
    # for png_file in images_dir.glob("*.png"):
    #   logging.info(f"Extracting {png_file.name}")
    #   result = ocr_main.extract_text_coordinates(png_file)
    #   result_list.extend(result)

    with open(self.file_name, "wb") as f:
      f.write(self.img_bytes)

    result = ocr_main.extract_text_coordinates(self.file_name)
    ocr_main.save_coordinate_map(result, self.ocr_map_path)

  def plan_redact(self):
    # self.validate()

    redaction_boxes = planner.analyze_and_map(self.ocr_map_path)
    planner.save_redact_plan(redaction_boxes)

  def apply_redact(self):
    # self.validate()

    painter.apply_redaction(self.file_name,
                            plan_path="redaction_plan.json", output_path="safe.png")





