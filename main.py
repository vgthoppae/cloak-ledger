import root_agent
import cloak_logger

def main():
  clog = cloak_logger.CloakLogger()
  clog.configure()

  ra = root_agent.RootAgent()

  try:
    # prompt input
    ra.prompt_input()

    # convert to png
    ra.convert_to_image()
    print("after image conversion")

    # do OCR
    ra.do_ocr()
    print("after ocr")

    ra.plan_redact()
    print("after redact plan")

    ra.apply_redact()
    print("after redact apply")

    # pdf_converter_main.convert_pdf_to_images(
    #   pdf_path="/Users/vgthoppae/Downloads/realistic_medical_invoice.pdf",
    #   output_folder="./source_images/")

    # ocr_main.extract_text_coordinates("./source_images")

  except Exception as e:
    print("Error:", "Sorry, the execution failed.")
    print(e)

if __name__ == "__main__":
  main()

