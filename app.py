import tempfile
import pandas as pd
import streamlit as st

from utils.file_handler import get_file_type, preview_image
from utils.ocr import extract_text_from_file
from utils.classifier import classify_document
from utils.extractor import extract_information
from utils.exporter import export_json, export_csv, export_excel

st.set_page_config(
    page_title="DeepVision",
    page_icon="📄",
    layout="wide"
)

st.title("📄 DeepVision")
st.subheader("OCR Intelligent Document Extraction")

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["jpg", "jpeg", "png", "pdf", "docx", "txt"]
)

if uploaded_file:

    st.success("File uploaded successfully!")

    file_type = get_file_type(uploaded_file)

    if file_type in ["jpg", "jpeg", "png"]:
        image = preview_image(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Extract Text"):

        suffix = "." + file_type if file_type else ".tmp"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getbuffer())
            temp_path = tmp.name

        with st.spinner("Extracting text..."):
            text = extract_text_from_file(temp_path, file_type)

        st.success("Extraction Completed")

        st.subheader("Extracted Text")
        st.text_area("", text, height=300)

        document_type = classify_document(text)

        st.subheader("Document Type")
        st.info(document_type)

        info = extract_information(text)

        st.subheader("Extracted Information")

        df = pd.DataFrame(
            list(info.items()),
            columns=["Field", "Value"]
        )

        st.table(df)

        st.subheader("JSON Output")
        st.code(export_json(info), language="json")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                "Download JSON",
                export_json(info),
                "output.json",
                "application/json"
            )

        with col2:
            st.download_button(
                "Download CSV",
                export_csv(info),
                "output.csv",
                "text/csv"
            )

        with col3:
            st.download_button(
                "Download Excel",
                export_excel(info),
                "output.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )