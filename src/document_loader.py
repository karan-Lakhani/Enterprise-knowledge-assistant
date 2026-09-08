from pathlib import Path
from pypdf import PdfReader


def load_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def load_documents(documents_folder):
    documents = []

    for pdf_file in Path(documents_folder).glob("*.pdf"):
        text = load_pdf(pdf_file)

        documents.append(
            {
                "filename": pdf_file.name,
                "text": text
            }
        )

    return documents