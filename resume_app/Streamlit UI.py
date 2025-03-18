import streamlit as st
from matcher import analyze_resume_against_job
from extractor import extract_company_name, extract_resume_text

st.title("📄 Resume vs Job Posting Analyzer")

# --- Resume Upload ---
uploaded_resume = st.file_uploader("📂 Upload Your Resume (PDF/DOCX)", type=["pdf", "docx"])

# --- Option to Paste Resume Instead (Hidden Initially) ---
show_paste_option = st.checkbox("Paste Resume Instead")

if show_paste_option:
    resume_text = st.text_area("✍ Paste your Resume Text", height=200)
else:
    resume_text = extract_resume_text(uploaded_resume)

# User Inputs
resume_text = st.text_area("Paste your Resume Text", height=200)
job_text = st.text_area("Paste Job Posting Text", height=200)

# Hidden job posting section
show_text = st.checkbox("Show Job Posting Text", value=False)

# Extract company name from job posting
company_name = extract_company_name(job_text)
st.subheader(f"🏢 Job Posting from: **{company_name}**")

if show_text:
    st.subheader("🔎 Extracted Job Posting Text")
    st.write(job_text)

if st.button("Analyze Resume"):
    if resume_text and job_text:
        # Run analysis
        match_results = analyze_resume_against_job(resume_text, job_text)

        # Display results
        st.subheader("🔍 Resume Matching Results")

        # Top Job Keywords
        st.write("### 🔹 **Top Keywords in Job Posting**")
        for word, count, score in match_results["top_job_keywords"]:
            st.write(f"**{word}**: {count} occurrences, Importance: {score}/10")

        # Top Job Bigrams
        st.write("### 🔹 **Top Bigrams in Job Posting**")
        for bigram, count, score in match_results["top_job_bigrams"]:
            st.write(f"**{bigram}**: {count} occurrences, Importance: {score}/10")

        # Keyword Matches
        st.write("### ✅ **Keyword Matches in Resume**")
        if match_results["keyword_matches"]:
            for word, count in match_results["keyword_matches"]:
                st.write(f"✔ **{word}**: {count} occurrences")
        else:
            st.write("⚠ No keyword matches found.")

        # Bigram Matches
        st.write("### 🔗 **Bigram Matches in Resume**")
        if match_results["bigram_matches"]:
            for bigram, count in match_results["bigram_matches"]:
                st.write(f"✔ **{bigram}**: {count} occurrences")
        else:
            st.write("⚠ No bigram matches found.")

        # Missing Important Keywords
        if match_results["missing_keywords"]:
            st.write("### ❌ **Missing Important Keywords**")
            st.write(", ".join(match_results["missing_keywords"]))

        # Missing Important Bigrams
        if match_results["missing_bigrams"]:
            st.write("### ❌ **Missing Important Bigrams**")
            st.write(", ".join(match_results["missing_bigrams"]))

    else:
        st.warning("⚠ Please paste both your resume and the job posting text.")
