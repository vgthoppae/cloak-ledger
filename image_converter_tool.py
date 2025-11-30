from pdf2image import convert_from_path
import io

def pdf_to_image(pdf_path: str = "/kaggle/input/invoice/realistic_medical_invoice.pdf", page: int = 0) -> dict:
    """
    Convert a PDF page to a PNG image and return the image as bytes.

    Args:
        pdf_path: Path to the PDF file within the notebook environment.
        page:     Zero-based index of the page to convert (0 = first page).

    Returns:
        {
          "filename": "input_page_<n>.png"
        }
    """
    # pdf2image uses 1-based page numbers
    page_number = page + 1

    images = convert_from_path(
        pdf_path,
        first_page=page_number,
        last_page=page_number,
    )

    if not images:
        raise ValueError(f"No page {page} found in {pdf_path}")

    img = images[0]

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()

    filename = f"{pdf_path.rsplit('/', 1)[-1].rsplit('.', 1)[0]}_page_{page}.png"

    upload_bytes_to_gcs(img_bytes, filename)

    return {
        "filename": filename,
    }