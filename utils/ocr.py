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

    print("========== LOADING OCR READER ==========")

    if reader is None:
        if easyocr is None:
            raise Exception("EasyOCR is not installed.")

        reader = easyocr.Reader(
            ["en"],
            gpu=False,
            verbose=True
        )

    print("========== OCR READER READY ==========")

    return reader


def preprocess_image(image_path):
    print("Preprocessing image...")

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

    print(f"Processing: {file_path}")
    print(f"Extension: {extension}")

    try:

        # ---------------- IMAGE ---------------- #

        if extension in [
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".tif",
            ".tiff"
        ]:

            print("STEP 1 - Image detected")

            image = preprocess_image(file_path)

            print("STEP 2 - Image preprocessed")

            reader = get_reader()

            print("STEP 3 - Starting OCR")

            results = reader.readtext(
                image,
                detail=1,
                paragraph=True
            )

            print("STEP 4 - OCR Finished")

            if not results:
                return "No text detected."

            text = "\n".join([r[1] for r in results])

            print("Characters extracted:", len(text))

            return text

        # ---------------- PDF ---------------- #

        elif extension == ".pdf":

            if fitz is None:
                return "PyMuPDF is not installed."

            pdf = fitz.open(file_path)

            final_text = ""

            reader = get_reader()

            for page_number in range(len(pdf)):

                print(f"Reading PDF Page {page_number + 1}")

                page = pdf.load_page(page_number)

                pix = page.get_pixmap(dpi=300)

                temp = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".png"
                )

                pix.save(temp.name)

                image = preprocess_image(temp.name)

                results = reader.readtext(
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
                return "python-docx is not installed."

            doc = Document(file_path)

            text = "\n".join(
                para.text
                for para in doc.paragraphs
            )

            return text

        # ---------------- TEXT FILES ---------------- #

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
            return f"Unsupported file type: {extension}"

    except Exception as e:

        import traceback

        print("========== OCR ERROR ==========")
        traceback.print_exc()

        return f"OCR Error: {str(e)}"