import streamlit as st
from matcher import analyze_resume_against_job
from extractor import extract_company_name, extract_resume_text

st.title("📄 Resume vs Job Posting Analyzer")

# --- Resume Upload ---
uploaded_resume = st.file_uploader("📂 Upload Your Resume (PDF/DOCX)", type=["pdf", "docx"])

# Extract resume text (automatically from the file)
resume_text = extract_resume_text(uploaded_resume) if uploaded_resume else ""

# Job Posting Input
job_text = st.text_area("📋 Paste Job Posting Text", height=200)

# --- Extract Company Name ---
company_name = extract_company_name(job_text)

# If no company is found, allow the user to enter it manually
if company_name == "Unknown Company":
    company_name = st.text_input("🏢 Company Name (Enter if not detected)", "")
    company_confirmed = bool(company_name.strip())  # Check if user entered something
else:
    st.subheader(f"🏢 Job Posting from: **{company_name}**")
    company_confirmed = True  # Company is valid

# --- Analyze Resume Button ---
if st.button("Analyze Resume"):
    if resume_text and job_text and company_confirmed:
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
        st.warning("⚠ Please upload a resume and paste the job posting text.")

