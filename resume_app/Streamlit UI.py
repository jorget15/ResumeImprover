import streamlit as st
from matcher import analyze_resume_against_job
from extractor import extract_resume_text
import os
import nltk

# 1) Provide a directory to store NLTK data
nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data")
os.makedirs(nltk_data_path, exist_ok=True)

# 2) Add the directory to NLTK's search path
if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)

# 3) Download the tagger + any other resources you need, e.g. "punkt", "wordnet", "omw-1.4"
nltk.download("averaged_perceptron_tagger_eng", download_dir=nltk_data_path)
nltk.download("punkt", download_dir=nltk_data_path)
nltk.download("wordnet", download_dir=nltk_data_path)
nltk.download("omw-1.4", download_dir=nltk_data_path)

# --- Your existing Streamlit code below ---
st.title("📄 Resume vs Job Posting Analyzer")
...

st.title("📄 Resume vs Job Posting Analyzer")

# --- Company Name ---
company_name = st.text_input("🏢 Enter the Company Name (Required)")

# --- Resume Upload ---
uploaded_resume = st.file_uploader("📂 Upload Your Resume (PDF/DOCX)", type=["pdf", "docx"])
resume_text = extract_resume_text(uploaded_resume) if uploaded_resume else ""

# --- Job Posting Input ---
job_text = st.text_area("📋 Paste Job Posting Text", height=200)

# --- Analyze Button ---
if st.button("Analyze Resume"):
    if not company_name.strip():
        st.warning(
            "⚠ Please enter the company name before analyzing. This helps exclude the company name from results.")
    elif not resume_text or not job_text.strip():
        st.warning("⚠ Please upload a resume and paste the job posting text.")
    else:
        # 1) Run analysis
        match_results = analyze_resume_against_job(resume_text, job_text, company_name)

        # 2) Display results
        st.subheader("🔍 Resume Matching Results")

        # Top Job Keywords
        st.write("### 🔹 **Top Keywords in Job Posting**")
        for word, count, score in match_results["top_job_keywords"]:
            st.write(f"**{word}**: {count} occurrences, Importance: {score}/10")

        # Top Job Bigrams
        st.write("### 🔹 **Top Bigrams in Job Posting**")
        for bigram, count, score in match_results["top_job_bigrams"]:
            st.write(f"**{bigram}**: {count} occurrences, Importance: {score}/10")

        # Top Resume Keywords
        st.write("### 📝 **Top Keywords in Resume**")
        if match_results["top_resume_keywords"]:
            for word, count, score in match_results["top_resume_keywords"]:
                st.write(f"**{word}**: {count} occurrences, Importance: {score}/10")
        else:
            st.write("⚠ No significant keywords found in resume.")

        # Top Resume Bigrams
        st.write("### 📝 **Top Bigrams in Resume**")
        if match_results["top_resume_bigrams"]:
            for bigram, count, score in match_results["top_resume_bigrams"]:
                st.write(f"**{bigram}**: {count} occurrences, Importance: {score}/10")
        else:
            st.write("⚠ No significant bigrams found in resume.")

        # Keyword Matches
        st.write("### ✅ **Keyword Matches in Resume**")
        if match_results["keyword_matches"]:
            for word, job_count in match_results["keyword_matches"]:
                st.write(f"✔ **{word}**: {job_count} occurrences (job posting side)")
        else:
            st.write("⚠ No keyword matches found.")

        # Bigram Matches
        st.write("### 🔗 **Bigram Matches in Resume**")
        if match_results["bigram_matches"]:
            for bigram, job_count in match_results["bigram_matches"]:
                st.write(f"✔ **{bigram}**: {job_count} occurrences (job posting side)")
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
