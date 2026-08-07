import os
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

try:
    import easyocr
except ImportError:
    easyocr = None

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from docx import Document
except ImportError:
    Document = None


reader = None


def get_reader():
    global reader

    if reader is None:
        if easyocr is None:
            raise Exception("EasyOCR is not installed.")

        reader = easyocr.Reader(["en"], gpu=False)

    return reader


def preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = image.resize(
        (image.width * 2, image.height * 2),
        Image.Resampling.LANCZOS
    )
    return np.array(image)


def extract_text(image_path):
    return extract_text_from_file(image_path)


def extract_text_from_file(file_path, file_type=None):

    extension = Path(file_path).suffix.lower()

    if file_type:
        extension = "." + file_type.split("/")[-1].lower()

    try:

        # ---------------- Images ---------------- #

        if extension in [
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".tif",
            ".tiff"
        ]:

            image = preprocess_image(file_path)

            results = get_reader().readtext(
                image,
                detail=1,
                paragraph=True
            )

            if len(results) == 0:
                return "No text detected."

            text = ""

            for r in results:
                text += r[1] + "\n"

            return text.strip()

        # ---------------- PDF ---------------- #

        elif extension == ".pdf":

            if fitz is None:
                return "PyMuPDF not installed."

            pdf = fitz.open(file_path)

            final_text = ""

            for page in pdf:

                pix = page.get_pixmap(dpi=300)

                temp = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".png"
                )

                pix.save(temp.name)

                image = preprocess_image(temp.name)

                results = get_reader().readtext(
                    image,
                    detail=1,
                    paragraph=True
                )

                for r in results:
                    final_text += r[1] + "\n"

                os.remove(temp.name)

            pdf.close()

            if final_text.strip() == "":
                return "No text detected."

            return final_text.strip()

        # ---------------- DOCX ---------------- #

        elif extension == ".docx":

            if Document is None:
                return "python-docx not installed."

            doc = Document(file_path)

            return "\n".join(
                p.text
                for p in doc.paragraphs
            )

        # ---------------- Text ---------------- #

        elif extension in [
            ".txt",
            ".csv",
            ".json",
            ".md",
            ".log"
        ]:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:
                return f.read()

        else:
            return "Unsupported file."

    except Exception as e:
        return f"OCR Error: {str(e)}"