import streamlit as st

from pdf_reader import extract_text_from_pdf
from resume_analyzer import (
    SECTION_ALIASES,
    detect_skills,
    detect_sections,
    calculate_score,
)
from ai_analyzer import analyze_with_ai


def show_list(items):
    for item in items:
        st.markdown("- " + str(item))


# ---------- Page setup ----------

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer")
st.write(
    "Upload a PDF resume to get a rule-based score, detected skills and sections, "
    "and AI-written feedback with suggestions for improvement."
)

# ---------- Upload and button ----------

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
analyze_clicked = st.button("Analyze Resume")

# ---------- Run the analysis ----------

if analyze_clicked:
    if uploaded_file is None:
        st.warning("Please upload a PDF resume first.")
        st.stop()

    # Station 1: PDF -> text
    try:
        resume_text = extract_text_from_pdf(uploaded_file)
    except Exception:
        st.error("Could not read this PDF. It may be damaged or password-protected.")
        st.stop()

    if len(resume_text.strip()) == 0:
        st.error("No text found. The PDF may be a scanned image. Try a PDF exported from Word or Google Docs.")
        st.stop()

    # Station 2: rule-based analysis
    skills = detect_skills(resume_text)
    sections = detect_sections(resume_text)
    total_score, breakdown = calculate_score(resume_text)

    missing_sections = []
    for section_name in SECTION_ALIASES:
        if section_name not in sections:
            missing_sections.append(section_name)

    st.divider()
    st.header("Rule-based analysis")

    st.metric("Resume Score", str(total_score) + " / 100")
    st.progress(min(total_score, 100) / 100)

    score_columns = st.columns(len(breakdown))
    index = 0
    for category, points in breakdown.items():
        score_columns[index].metric(category, points)
        index += 1

    left, right = st.columns(2)

    with left:
        st.subheader("Detected skills")
        if skills:
            st.write(", ".join(skills))
        else:
            st.write("No skills from our list were found.")

    with right:
        st.subheader("Detected sections")
        if sections:
            st.write(", ".join(sections))
        else:
            st.write("No standard sections found.")
        if missing_sections:
            st.caption("Not found: " + ", ".join(missing_sections))
with st.expander("How does this work?"):
    st.markdown(
        "1. **PDF reader** extracts the text from your resume.\n"
        "2. **Rule-based Python** finds skills and sections and calculates the score. "
        "No machine learning is used here.\n"
        "3. **A pretrained AI model** (through an API) writes the feedback. "
        "No model is trained in this project."
    )
    # Station 3: AI feedback
    st.divider()
    st.header("AI feedback")

    with st.spinner("Asking the AI to review your resume..."):
        ai_result = analyze_with_ai(resume_text)

    if "error" in ai_result:
        st.warning("AI feedback is unavailable right now. The rule-based results above still work.")
        st.caption("Details: " + str(ai_result["error"])[:300])
    else:
        st.success("Recommended job role: " + str(ai_result.get("suggested_job_role", "Not available")))

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("💪 Strengths")
            show_list(ai_result.get("strengths", []))
        with col2:
            st.subheader("⚠️ Weaknesses")
            show_list(ai_result.get("weaknesses", []))

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("🧩 Missing skills")
            show_list(ai_result.get("missing_skills", []))
        with col4:
            st.subheader("🚀 Improvement suggestions")
            show_list(ai_result.get("improvement_suggestions", []))