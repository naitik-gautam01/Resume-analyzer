from pypdf import PdfReader


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)

    all_text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            all_text = all_text + page_text + "\n"

    return all_text.strip()