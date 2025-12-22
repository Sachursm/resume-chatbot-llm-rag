from pypdf import PdfReader

def load_pdf_text(pdf_path: str) -> str: #return type string
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    if not text.strip():
        raise ValueError("PDF contains no extractable text")

    return text
