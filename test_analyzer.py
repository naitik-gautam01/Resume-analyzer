from pdf_reader import extract_text_from_pdf
from resume_analyzer import detect_skills, detect_sections, check_keywords

text = extract_text_from_pdf("resumes/Neelashish_resume.pdf")

print(len(text))
print("Skills found:", detect_skills(text))
print("Sections found:", detect_sections(text))

present, missing, has_email = check_keywords(text)
print("Keywords present:", present)
print("Keywords missing:", missing)
print("Has email:", has_email)

if len(text.strip()) == 0:
    print("No text could be extracted. The PDF may be damaged or scanned.")
else:
    print("Skills found:", detect_skills(text))
from resume_analyzer import calculate_score

total, breakdown = calculate_score(text)
print("Total score:", total, "/ 100")
for category, points in breakdown.items():
    print(" ", category, ":", points)