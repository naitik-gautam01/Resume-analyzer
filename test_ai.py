from pdf_reader import extract_text_from_pdf
from ai_analyzer import analyze_with_ai

text = extract_text_from_pdf("resumes/Neelashish_Resume.pdf")
result = analyze_with_ai(text)

if "error" in result:
    print("PROBLEM:", result["error"])
else:
    print("Job role:", result["suggested_job_role"])
    print("Strengths:", result["strengths"])
    print("Weaknesses:", result["weaknesses"])
    print("Missing skills:", result["missing_skills"])
    print("Suggestions:", result["improvement_suggestions"])