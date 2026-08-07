import re

def extract_information(text):
    info = {
        "Email": "",
        "Phone": "",
        "Date": "",
        "Amount": ""
    }

    # Email
    email = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )
    if email:
        info["Email"] = email.group()

    # Phone
    phone = re.search(
        r"\b\d{10}\b",
        text
    )
    if phone:
        info["Phone"] = phone.group()

    # Date
    date = re.search(
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        text
    )
    if date:
        info["Date"] = date.group()

    # Amount
    amount = re.search(
        r"₹?\s?\d+(?:,\d{3})*(?:\.\d{2})?",
        text
    )
    if amount:
        info["Amount"] = amount.group()

    return info