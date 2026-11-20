import os

from pdf_reader import extract_text_from_pdf
from resume_analyzer import detect_skills, detect_sections, calculate_score

folder = "resumes"

for file_name in os.listdir(folder):
    if not file_name.lower().endswith(".pdf"):
        continue

    path = folder + "/" + file_name
    print("=" * 50)
    print("FILE:", file_name)

    try:
        text = extract_text_from_pdf(path)
    except Exception as error:
        print("  FAILED to read PDF:", error)
        continue

    if len(text.strip()) == 0:
        print("  No text found (scanned or empty PDF)")
        continue

    total, breakdown = calculate_score(text)
    print("  Characters:", len(text))
    print("  Score:", total, breakdown)
    print("  Sections:", detect_sections(text))
    print("  Skills:", detect_skills(text))