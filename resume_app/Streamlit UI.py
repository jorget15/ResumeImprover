import streamlit as st
from matcher import analyze_resume_against_job
from extractor import extract_company_name, extract_resume_text

st.title("📄 Resume vs Job Posting Analyzer")

# --- Resume Upload (No Paste Option) ---
uploaded_resume = st.file_uploader("📂 Upload Your Resume (PDF/DOCX)", type=["pdf", "docx"])

resume_text = ""
if uploaded_resume:
    resume_text = extract_resume_text(uploaded_resume)

# --- Job Posting Input (Fix for Broken Textbox) ---
job_text = st.text_area("📋 Paste Job Posting Text Here", value="", height=200)

# --- Initialize Company Name (Hidden Initially) ---
company_name = extract_company_name(job_text) if job_text else ""
show_company_input = False  # Hide company input until analysis

# --- Analyze Button ---
if st.button("🔍 Analyze Resume"):
    if not resume_text.strip():
        st.warning("⚠ Please upload a resume.")
    elif not job_text.strip():
        st.warning("⚠ Please paste the job posting text.")
    else:
        # Run analysis
        match_results = analyze_resume_against_job(resume_text, job_text)

        # Show Company Name Input Field After Analysis
        show_company_input = True  # Now allow user input

        # --- Display Results ---
        st.subheader("🔍 Resume Matching Results")

        # Company Name Input Field (Editable)
        company_name = st.text_input("🏢 Company Name:", value=company_name, placeholder="Enter company name")

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
