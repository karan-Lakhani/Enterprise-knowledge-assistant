import re


def get_category(filename):
    filename = filename.lower()

    if "leave" in filename or "handbook" in filename:
        return "HR"

    if "expense" in filename:
        return "Finance"

    if "vpn" in filename:
        return "Security"

    if "incident" in filename:
        return "Operations"

    if "product" in filename:
        return "Product"

    return "General"


def chunk_text(text):

    # Split on numbered section headings
    sections = re.split(
        r'(?=\b\d+\.\d+\b)',
        text
    )

    chunks = []

    for section in sections:

        section = section.strip()

        if len(section) < 100:
            continue

        chunks.append(section)

    return chunks


def chunk_document(document):

    chunks = chunk_text(
        document["text"]
    )

    chunk_objects = []

    for idx, chunk in enumerate(chunks):

        chunk_objects.append(
            {
                "chunk_id": f"{document['filename']}_{idx}",
                "source": document["filename"],
                "category": get_category(document["filename"]),
                "section_title": extract_section_title(chunk),
                "text": chunk
            }
        )

    return chunk_objects

def extract_section_title(text):
    first_line = text.split("\n")[0].strip()
    return first_line[:150]