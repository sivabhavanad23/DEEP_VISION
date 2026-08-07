from PIL import Image
import fitz  # PyMuPDF
import pandas as pd
from docx import Document


def get_file_type(uploaded_file):
    """Returns the file extension."""
    return uploaded_file.name.split(".")[-1].lower()


# -----------------------------
# IMAGE
# -----------------------------
def preview_image(uploaded_file):
    return Image.open(uploaded_file)


# -----------------------------
# PDF
# -----------------------------
def preview_pdf(uploaded_file):
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    page = pdf.load_page(0)

    pix = page.get_pixmap(dpi=200)

    image = Image.frombytes(
        "RGB",
        [pix.width, pix.height],
        pix.samples
    )

    pdf.close()

    return image


# -----------------------------
# DOCX
# -----------------------------
def read_docx(uploaded_file):
    doc = Document(uploaded_file)

    text = ""

    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"

    return text


# -----------------------------
# TXT
# -----------------------------
def read_txt(uploaded_file):
    return uploaded_file.read().decode("utf-8")


# -----------------------------
# CSV
# -----------------------------
def read_csv(uploaded_file):
    return pd.read_csv(uploaded_file)


# -----------------------------
# EXCEL
# -----------------------------
def read_excel(uploaded_file):
    return pd.read_excel(uploaded_file)