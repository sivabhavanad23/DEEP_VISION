import importlib
import os
import tempfile
from pathlib import Path

_reader = None


def _load_module(module_name):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


def _get_reader():
    global _reader
    if _reader is None:
        easyocr = _load_module("easyocr")
        if easyocr is None:
            raise RuntimeError("easyocr is not installed")

        _reader = easyocr.Reader(["en"], gpu=False)

    return _reader


def preprocess_image(image_path):
    """
    Improve image quality before OCR.
    """

    cv2 = _load_module("cv2")
    if cv2 is None:
        raise RuntimeError("OpenCV is not installed")

    image = cv2.imread(image_path)

    if image is None:
        raise Exception("Unable to read image.")

    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.fastNlMeansDenoising(gray)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )
    return thresh


def extract_text(image_path):
    """
    Extract text from image using EasyOCR.
    """

    try:
        processed_image = preprocess_image(image_path)
        results = _get_reader().readtext(processed_image, detail=1, paragraph=True)

        extracted_text = ""
        for result in results:
            extracted_text += result[1] + "\n"

        if extracted_text.strip() == "":
            return "No text detected."

        return extracted_text.strip()

    except Exception as exc:
        return f"OCR Error: {str(exc)}"


def extract_text_from_file(file_path, file_type=None):
    """
    Extract text from an uploaded image, PDF, DOCX, or text file.
    """

    try:
        ext = (file_type or Path(file_path).suffix.lower().lstrip("."))
        ext = ext.lower().split("/")[-1]

        if ext in {"png", "jpg", "jpeg", "bmp", "tif", "tiff"}:
            return extract_text(file_path)

        if ext == "pdf":
            fitz = _load_module("fitz")
            if fitz is None:
                return "PDF support requires PyMuPDF."

            pdf = fitz.open(file_path)
            pages = []
            try:
                for page_number in range(len(pdf)):
                    page = pdf.load_page(page_number)
                    pix = page.get_pixmap(dpi=300)
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                        temp_path = temp_file.name
                    pix.save(temp_path)
                    try:
                        pages.append(extract_text(temp_path))
                    finally:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
            finally:
                pdf.close()

            return "\n\n".join(page for page in pages if page).strip() or "No text detected."

        if ext == "docx":
            docx = _load_module("docx")
            if docx is None:
                return "DOCX support requires python-docx."

            document = docx.Document(file_path)
            paragraphs = [para.text.strip() for para in document.paragraphs if para.text.strip()]
            return "\n".join(paragraphs)

        if ext in {"txt", "md", "json", "csv", "log"}:
            with open(file_path, "r", encoding="utf-8") as handle:
                return handle.read().strip()

        return f"Unsupported file type: {ext or 'unknown'}"

    except Exception as exc:
        return f"OCR Error: {str(exc)}"