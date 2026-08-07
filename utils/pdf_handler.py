import fitz  # PyMuPDF
from PIL import Image
import tempfile


def pdf_to_images(uploaded_file):
    """
    Convert every page of a PDF into images.
    """

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    image_paths = []

    for page_num in range(len(pdf)):

        page = pdf.load_page(page_num)

        pix = page.get_pixmap(dpi=300)

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".png"
        )

        pix.save(temp.name)

        image_paths.append(temp.name)

    pdf.close()

    return image_paths