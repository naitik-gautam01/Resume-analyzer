from pdf_reader import extract_text_from_pdf

text = extract_text_from_pdf("resumes/Neelashish_Resume.pdf")

print(text)
print("-----")
print("Number of characters:", len(text))