import re
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_information(text):

    doc = nlp(text)

    data = {}

    # -------------------------
    # PERSON NAME
    # -------------------------

    for ent in doc.ents:

        if ent.label_ == "PERSON":
            data["Name"] = ent.text
            break

    # -------------------------
    # EMAIL
    # -------------------------

    email = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    data["Email"] = email[0] if email else ""

    # -------------------------
    # PHONE
    # -------------------------

    phone = re.findall(
        r"\+?\d[\d\s\-]{8,15}",
        text
    )

    data["Phone"] = phone[0] if phone else ""

    # -------------------------
    # DATE
    # -------------------------

    date = re.findall(
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
        text
    )

    data["Date"] = date[0] if date else ""

    # -------------------------
    # AMOUNT
    # -------------------------

    amount = re.findall(
        r"(?:Rs\.?|INR)?\s?\d+(?:,\d{3})*(?:\.\d{2})?",
        text
    )

    data["Amount"] = amount[0] if amount else ""

    return data