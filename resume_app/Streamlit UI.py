import streamlit as st
from matcher import analyze_resume_against_job
from extractor import extract_company_name, extract_resume_text

st.title("📄 Resume vs Job Posting Analyzer")

# --- Resume Upload ---
uploaded_resume = st.file_uploader("📂 Upload Your Resume (PDF/DOCX)", type=["pdf", "docx"])

resume_text = ""
if uploaded_resume:
    resume_text = extract_resume_text(uploaded_resume)  # Extract only if uploaded

# --- Job Posting Input ---
job_text = st.text_area("📋 Paste Job Posting Text Here", height=200, value="")

# --- Hide Company Name Until Analysis is Done ---
show_company_input = False

if st.button("Analyze Resume"):
    if resume_text and job_text:
        match_results = analyze_resume_against_job(resume_text, job_text)

        # Extract company name after analyzing
        company_name = extract_company_name(job_text)

        # Show company name only after analysis
        if company_name:
            st.subheader(f"🏢 Job Posting from: **{company_name}**")

        # Show results
        st.subheader("🔍 Resume Matching Results")
        st.write("### 🔹 **Top Keywords in Job Posting**")
        for word, count, score in match_results["top_job_keywords"]:
            st.write(f"**{word}**: {count} occurrences, Importance: {score}/10")

        st.write("### 🔹 **Top Bigrams in Job Posting**")
        for bigram, count, score in match_results["top_job_bigrams"]:
            st.write(f"**{bigram}**: {count} occurrences, Importance: {score}/10")

        st.write("### ✅ **Keyword Matches in Resume**")
        if match_results["keyword_matches"]:
            for word, count in match_results["keyword_matches"]:
                st.write(f"✔ **{word}**: {count} occurrences")
        else:
            st.write("⚠ No keyword matches found.")

        st.write("### 🔗 **Bigram Matches in Resume**")
        if match_results["bigram_matches"]:
            for bigram, count in match_results["bigram_matches"]:
                st.write(f"✔ **{bigram}**: {count} occurrences")
        else:
            st.write("⚠ No bigram matches found.")

        if match_results["missing_keywords"]:
            st.write("### ❌ **Missing Important Keywords**")
            st.write(", ".join(match_results["missing_keywords"]))

        if match_results["missing_bigrams"]:
            st.write("### ❌ **Missing Important Bigrams**")
            st.write(", ".join(match_results["missing_bigrams"]))

    else:
        st.warning("⚠ Please upload a resume and paste the job posting text.")
