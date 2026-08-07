from utils.ocr import extract_text, extract_text_from_file


def test_extract_text_returns_error_for_missing_image(tmp_path):
    missing_path = tmp_path / "missing.png"
    result = extract_text(str(missing_path))
    assert "Unable to read" in result


def test_extract_text_from_file_reads_plain_text_files(tmp_path):
    sample_path = tmp_path / "sample.txt"
    sample_path.write_text("Hello DeepVision", encoding="utf-8")

    result = extract_text_from_file(str(sample_path), "txt")

    assert "Hello DeepVision" in result
