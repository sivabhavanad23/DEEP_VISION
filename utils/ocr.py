import os
import tempfile
from pathlib import Path

import cv2
import easyocr
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
from docx import Document

# -----------------------------
# Lazy Load EasyOCR
# -----------------------------
reader = None


def get_reader():
    global reader

    if reader is None:
        reader = easyocr.Reader(
            ["en"],
            gpu=False,
            download_enabled=True
        )

    return reader


# -----------------------------
# Image Preprocessing
# -----------------------------
def preprocess_image(image_path):
    """
    Improve OCR accuracy.
    """

    image = Image.open(image_path).convert("RGB")

    image = image.resize(
        (image.width * 2, image.height * 2),
        Image.Resampling.LANCZOS
    )

    image = np.array(image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    gray = cv2.equalizeHist(gray)

    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh


# -----------------------------
# Compatibility Function
# -----------------------------
def extract_text(image_path):
    return extract_text_from_file(image_path)


# -----------------------------
# OCR Main Function
# -----------------------------
def extract_text_from_file(file_path, file_type=None):

    extension = Path(file_path).suffix.lower()

    if file_type:
        extension = "." + file_type.split("/")[-1].lower()

    try:

        # =============================
        # IMAGE
        # =============================
        if extension in [
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".tif",
            ".tiff"
        ]:

            processed = preprocess_image(file_path)

            results = get_reader().readtext(
                processed,
                detail=1,
                paragraph=True
            )

            if len(results) == 0:
                return "No text detected."

            text = "\n".join(
                item[1]
                for item in results
            )

            return text

        # =============================
        # PDF
        # =============================
        elif extension == ".pdf":

            pdf = fitz.open(file_path)

            final_text = ""

            for page in pdf:

                pix = page.get_pixmap(dpi=300)

                temp = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".png"
                )

                pix.save(temp.name)

                processed = preprocess_image(temp.name)

                results = get_reader().readtext(
                    processed,
                    detail=1,
                    paragraph=True
                )

                for item in results:
                    final_text += item[1] + "\n"

                os.remove(temp.name)

            pdf.close()

            if final_text.strip() == "":
                return "No text detected."

            return final_text.strip()

        # =============================
        # DOCX
        # =============================
        elif extension == ".docx":

            document = Document(file_path)

            text = "\n".join(
                para.text
                for para in document.paragraphs
            )

            return text.strip()

        # =============================
        # TEXT FILES
        # =============================
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
            ) as file:

                return file.read()

        else:
            return "Unsupported file type."

    except Exception as e:
        return f"OCR Error: {str(e)}"