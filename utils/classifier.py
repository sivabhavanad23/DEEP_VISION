def classify_document(text):

    text = text.lower()

    if "invoice" in text:
        return "Invoice"

    elif "resume" in text:
        return "Resume"

    elif "aadhaar" in text:
        return "Aadhaar Card"

    elif "pan" in text:
        return "PAN Card"

    elif "passport" in text:
        return "Passport"

    elif "bank" in text:
        return "Bank Statement"

    else:
        return "Unknown Document"