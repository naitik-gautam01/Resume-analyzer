# AI Resume Analyzer

A Streamlit web app that analyzes a PDF resume using rule-based Python
and a pretrained AI model accessed through an API.

## Features
- Extracts text from any text-based PDF resume
- Detects skills and resume sections (rule-based)
- Calculates a score out of 100 with a breakdown (rule-based)
- AI-written strengths, weaknesses, missing skills, suggested job role and tips
- Works on new resumes at runtime. No training dataset is needed.

## How it works
1. `pdf_reader.py` converts the PDF into text (pypdf).
2. `resume_analyzer.py` finds skills and sections and calculates the score.
3. `ai_analyzer.py` sends the text to the Gemini API and parses the JSON reply.
4. `app.py` displays everything with Streamlit.

**Rule-based vs AI:** the score, skills and sections come from plain Python rules
that I wrote, not from machine learning. Only the written feedback comes from a
pretrained model (inference only, no training).

## Setup
1. Clone the project and open the folder.
2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install libraries:
   ```
   pip install -r requirements.txt
   ```
4. Get a free API key from Google AI Studio.
5. Copy `.env.example` to `.env` and put your key in it.
6. Run:
   ```
   streamlit run app.py
   ```

## Project structure
```
app.py               Streamlit interface
pdf_reader.py        PDF to text
resume_analyzer.py   skills, sections, scoring
ai_analyzer.py       AI API call
.env.example         settings template (copy to .env)
```

## Scoring (100 points)
| Category | Max | Rule |
|---|---|---|
| Sections | 40 | education 8, skills 8, projects 8, experience 10, summary 6 |
| Skills | 30 | 3 points per skill found |
| Contact and links | 20 | email 8, GitHub 6, LinkedIn 6 |
| Length | 10 | 250-900 words |

The weights are my own design choices.

## Limitations
- Only skills from a fixed list are detected.
- Scanned (image) PDFs are not supported (OCR would be needed).
- Two-column layouts can mix up the text order.
- The free AI service can be slow or busy; the app retries and shows the
  rule-based results even if the AI fails.
- Do not upload real personal resumes you want to keep private, since the text is
  sent to an external AI service.

## Future improvements
- Compare a resume against a pasted job description
- OCR support for scanned PDFs
- Export the report as PDF
