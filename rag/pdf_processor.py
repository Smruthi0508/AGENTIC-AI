
import pymupdf
import os


def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    document = pymupdf.open(pdf_path)
    full_text = ""

    for page_number, page in enumerate(document):
        full_text += f"\n--- Page {page_number + 1} ---\n"
        full_text += page.get_text()

    document.close()
    return full_text


if __name__ == "__main__":
    pdf_path = "data/uploaded_papers/sample.pdf"

    text = extract_text_from_pdf(pdf_path)

    print("\nPDF extraction successful!")
    print(f"Total characters extracted: {len(text)}")
    print("\nFirst 1000 characters:\n")
    print(text[:1000])
