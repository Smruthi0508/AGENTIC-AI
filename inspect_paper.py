
import re
from rag.pdf_processor import extract_text_from_pdf

pdf_path = "data/uploaded_papers/sample.pdf"

text = extract_text_from_pdf(pdf_path)

print("\n========== RESEARCH PAPER HEADINGS ==========\n")

heading_pattern = re.compile(
    r"^(?:\d+(?:\.\d+)*\.?\s+)?"
    r"[A-Z][A-Za-z][A-Za-z0-9 &,:()'-]{1,75}$"
)

for line in text.splitlines():

    line = line.strip()

    if not line:
        continue

    if line.lower() in [
        "abstract",
        "references",
        "conclusion"
    ]:
        print(line)
        continue

    if heading_pattern.match(line):
        print(line)

print("\n========== INSPECTION COMPLETE ==========")
