import re


def classify_document(text):

    text = text.lower()

    if any(word in text for word in [
        "invoice",
        "gst",
        "invoice number",
        "tax invoice",
        "subtotal",
        "total amount"
    ]):
        return "Invoice"

    elif any(word in text for word in [
        "resume",
        "education",
        "experience",
        "skills",
        "projects"
    ]):
        return "Resume"

    elif "government of india" in text and "aadhaar" in text:
        return "Aadhaar Card"

    elif "income tax department" in text and "permanent account number" in text:
        return "PAN Card"

    elif "passport" in text:
        return "Passport"

    elif any(word in text for word in [
        "receipt",
        "cash receipt",
        "payment received"
    ]):
        return "Receipt"

    return "Unknown Document"