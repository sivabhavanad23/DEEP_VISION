import os
import json
import tempfile

import streamlit as st
from PIL import Image

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="DeepVision OCR",
    page_icon="📄",
    layout="wide"
)

# ---------------------------
# Dependency Check
# ---------------------------
try:
    import cv2
    cv2_status = f"✅ OpenCV {cv2.__version__} Loaded Successfully"
except Exception as e:
    st.error(f"❌ OpenCV Import Error:\n\n{e}")
    st.stop()

# ---------------------------
# Import Project Modules
# ---------------------------
try:
    from utils.ocr import extract_text_from_file
    from utils.extractor import extract_information
    from utils.classifier import classify_document
except Exception as e:
    st.error(f"❌ Project Import Error:\n\n{e}")
    st.stop()

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("📄 DeepVision")
st.sidebar.write("OCR Intelligent Document Extraction")
st.sidebar.success(cv2_status)

# ---------------------------
# Main Title
# ---------------------------
st.title("📄 DeepVision")
st.subheader("OCR Intelligent Document Extraction")

uploaded_file = st.file_uploader(
    "Upload a document",
    type=[
        "png",
        "jpg",
        "jpeg",
        "pdf",
        "docx",
        "txt",
        "csv",
        "json"
    ]
)

# ---------------------------
# Upload
# ---------------------------
if uploaded_file is not None:

    extension = os.path.splitext(uploaded_file.name)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension
    ) as temp_file:

        temp_file.write(uploaded_file.read())
        file_path = temp_file.name

    st.success("✅ File Uploaded Successfully")

    # Show image preview
    if extension.lower() in [".png", ".jpg", ".jpeg"]:
        image = Image.open(file_path)
        st.image(
            image,
            caption="Uploaded Image",
            width="stretch"
        )

    # OCR
    if st.button("Extract Text"):

        with st.spinner("Performing OCR..."):

            text = extract_text_from_file(file_path)

        st.success("Extraction Completed")

        st.subheader("Extracted Text")

        st.text_area(
            "OCR Output",
            value=text,
            height=300
        )

        document_type = classify_document(text)

        st.subheader("Document Type")
        st.info(document_type)

        information = extract_information(text)

        st.subheader("Extracted Information")

        st.table({
            "Field": list(information.keys()),
            "Value": list(information.values())
        })

        st.subheader("JSON Output")

        st.code(
            json.dumps(
                information,
                indent=4
            ),
            language="json"
        )

        st.download_button(
            label="📥 Download Extracted Text",
            data=text,
            file_name="Extracted_Text.txt",
            mime="text/plain"
        )

    if os.path.exists(file_path):
        os.remove(file_path)

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.caption("Developed by Siva Bhavana Dachepalli")