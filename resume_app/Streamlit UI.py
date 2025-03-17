import streamlit as st
from extractor import extract_keywords, extract_bigrams
from matcher import analyze_resume_against_job
import pdfplumber
from docx import Document


def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file."""
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(uploaded_file):
    """Extracts text from an uploaded DOCX file."""
    doc = Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])


# Streamlit UI setup
st.title("📄 Resume Improver")
st.write("Upload your resume and paste a job description to analyze how well they match!")

# Upload Resume
uploaded_resume = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
resume_text = ""
if uploaded_resume:
    if uploaded_resume.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_resume)
    elif uploaded_resume.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_text_from_docx(uploaded_resume)
    st.text_area("Extracted Resume Text:", resume_text, height=200)

# Input Job Description
job_text = st.text_area("Paste Job Description Here:", height=200)

if st.button("Analyze Resume"):
    if resume_text and job_text:
        # Run the matching analysis
        match_results = analyze_resume_against_job(resume_text, job_text)

        # Display Results
        st.subheader("🔍 Resume Matching Results")

        st.write("### ✅ Keyword Matches")
        for word, count in match_results["keyword_matches"].items():
            st.write(f"- {word}: {count} occurrences")

        st.write("### 🔗 Bigram Matches")
        for bigram, count in match_results["bigram_matches"].items():
            st.write(f"- {bigram}: {count} occurrences")

        st.write("### ❌ Missing Keywords")
        st.write(", ".join(match_results["missing_keywords"]))

        st.write("### ❌ Missing Bigrams")
        st.write(", ".join(match_results["missing_bigrams"]))
    else:
        st.warning("Please upload a resume and paste a job description before analyzing.")
