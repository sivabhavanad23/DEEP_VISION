import json
import pandas as pd
import io


def export_json(data):
    """Return formatted JSON string."""
    return json.dumps(data, indent=4)


def export_csv(data):
    """Return CSV data as bytes."""
    df = pd.DataFrame([data])
    return df.to_csv(index=False).encode("utf-8")


def export_excel(data):
    """Return Excel data as bytes."""
    df = pd.DataFrame([data])

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Extracted Data")

    output.seek(0)
    return output.getvalue()