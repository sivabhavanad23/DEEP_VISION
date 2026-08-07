from docx import Document


def extract_doc_text(uploaded_file):

    document = Document(uploaded_file)

    text = ""

    for para in document.paragraphs:

        text += para.text + "\n"

    return text