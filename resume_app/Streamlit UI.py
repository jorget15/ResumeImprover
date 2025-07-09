import streamlit as st
from matcher import analyze_resume_against_job
from extractor import extract_resume_text

# Page configuration
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(52, 73, 94, 0.3);
    }
    .section-header {
        background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 1rem 0 0.5rem 0;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.2);
    }
    .metric-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    .success-card {
        background: #e6f3ff;
        border: 1px solid #3498db;
        border-radius: 5px;
        padding: 0.75rem;
        margin: 0.25rem 0;
        color: #2c3e50;
    }
    .warning-card {
        background: #f1f5f9;
        border: 1px solid #64748b;
        border-radius: 5px;
        padding: 0.75rem;
        margin: 0.25rem 0;
        color: #475569;
    }
    .danger-card {
        background: #f8fafc;
        border: 1px solid #64748b;
        border-radius: 5px;
        padding: 0.75rem;
        margin: 0.25rem 0;
        color: #334155;
    }
    .stButton > button {
        background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 3px 10px rgba(52, 152, 219, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
        background: linear-gradient(135deg, #2980b9 0%, #1a252f 100%);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>📄 Resume vs Job Posting Analyzer</h1>
    <p>Optimize your resume to match job requirements perfectly</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with instructions and tips
with st.sidebar:
    st.markdown("### 📖 How to Use")
    st.markdown("""
    1. **Enter Company Name**: This helps filter out company-specific terms from analysis
    2. **Upload Resume**: Support for PDF and DOCX formats
    3. **Paste Job Posting**: Copy the complete job description
    4. **Click Analyze**: Get detailed matching insights
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Pro Tips")
    st.markdown("""
    - Use the **exact** keywords from job postings
    - Focus on **high-importance** keywords (8+ score)
    - Include keywords in **context**, not just lists
    - Review the **missing elements** tab for improvements
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Score Guide")
    st.markdown("""
    - **🟢 8-10**: Critical keywords - must include
    - **🟡 6-7**: Important keywords - should include  
    - **🔴 1-5**: Nice to have keywords
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This tool analyzes the alignment between your resume and job postings using advanced text processing to identify key terms and phrases that recruiters and ATS systems look for.
    """)

# Create two columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="section-header"><h3>📋 Job Information</h3></div>', unsafe_allow_html=True)
    
    # Company Name input
    company_name = st.text_input("🏢 Company Name", placeholder="Enter the company name...")
    
    # Job Posting Input
    job_text = st.text_area("📋 Job Posting", height=300, placeholder="Paste the complete job posting here...")

with col2:
    st.markdown('<div class="section-header"><h3>📄 Resume Upload</h3></div>', unsafe_allow_html=True)
    
    # Resume Upload button
    uploaded_resume = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], help="Supported formats: PDF, DOCX")
    resume_text = extract_resume_text(uploaded_resume) if uploaded_resume else ""
    
    if uploaded_resume:
        st.success(f"✅ Resume uploaded: {uploaded_resume.name}")
        with st.expander("📖 Preview Resume Text"):
            st.text_area("Resume Content", resume_text[:500] + "..." if len(resume_text) > 500 else resume_text, height=200, disabled=True)

# Center the analyze button
st.markdown("<br>", unsafe_allow_html=True)
col_center = st.columns([1, 2, 1])
with col_center[1]:
    # Analyze Button
    if st.button("🔍 Analyze Resume", use_container_width=True):
        if not company_name.strip(): #Checks if there is a company name and tells the user to input one if there isn't
            st.warning(
                "⚠ Please enter the company name before analyzing. This helps exclude the company name from results.")
        elif not resume_text or not job_text.strip():
            st.warning("⚠ Please upload a resume and paste the job posting text.")
        else:
            # Show progress
            with st.spinner('🔍 Analyzing your resume...'):
                # 1) Run analysis (calls Matcher.py's analyze_resume_against_job)
                match_results = analyze_resume_against_job(resume_text, job_text, company_name)

            # 2) Display results with improved styling
            st.balloons()  # Celebration animation
            st.markdown("---")
            st.markdown('<div class="section-header"><h2>🔍 Analysis Results</h2></div>', unsafe_allow_html=True)

            # Create tabs for better organization
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Job Keywords", "📝 Resume Analysis", "❌ Missing Elements"])

            with tab1:
                st.markdown("### 📈 Match Summary")
                
                # Create metrics row
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    keyword_matches = len(match_results["keyword_matches"]) if match_results["keyword_matches"] else 0
                    st.metric("🎯 Keyword Matches", keyword_matches)
                    
                with metric_col2:
                    bigram_matches = len(match_results["bigram_matches"]) if match_results["bigram_matches"] else 0
                    st.metric("🔗 Phrase Matches", bigram_matches)
                    
                with metric_col3:
                    missing_keywords = len(match_results["missing_keywords"]) if match_results["missing_keywords"] else 0
                    st.metric("⚠️ Missing Keywords", missing_keywords)
                    
                with metric_col4:
                    missing_bigrams = len(match_results["missing_bigrams"]) if match_results["missing_bigrams"] else 0
                    st.metric("⚠️ Missing Phrases", missing_bigrams)

                # Match percentage calculation
                total_job_keywords = len(match_results["top_job_keywords"])
                total_job_bigrams = len(match_results["top_job_bigrams"])
                total_elements = total_job_keywords + total_job_bigrams
                matched_elements = keyword_matches + bigram_matches
                
                if total_elements > 0:
                    match_percentage = (matched_elements / total_elements) * 100
                    st.markdown(f"### 🎯 Overall Match Score: {match_percentage:.1f}%")
                    st.progress(match_percentage / 100)
                    
                    if match_percentage >= 80:
                        st.success("🎉 Excellent match! Your resume aligns very well with the job requirements.")
                    elif match_percentage >= 60:
                        st.info("👍 Good match! Consider adding some missing keywords to improve further.")
                    elif match_percentage >= 40:
                        st.warning("⚠️ Moderate match. Your resume could benefit from more relevant keywords.")
                    else:
                        st.error("❌ Low match. Consider significantly revising your resume to better align with this position.")

            with tab2:
                # Top Job Keywords
                st.markdown("### 🔹 **Top Keywords in Job Posting**")
                if match_results["top_job_keywords"]:
                    for i, (word, count, score) in enumerate(match_results["top_job_keywords"], 1):
                        score_color = "🟢" if score >= 8 else "🟡" if score >= 6 else "🔴"
                        st.markdown(f"""
                        <div class="metric-card">
                            <strong>#{i} {word}</strong> {score_color}<br>
                            📊 {count} occurrences | ⭐ Importance: {score}/10
                        </div>
                        """, unsafe_allow_html=True)

                # Top Job Bigrams
                st.markdown("### 🔹 **Top Phrases in Job Posting**")
                if match_results["top_job_bigrams"]:
                    for i, (bigram, count, score) in enumerate(match_results["top_job_bigrams"], 1):
                        score_color = "🟢" if score >= 8 else "🟡" if score >= 6 else "🔴"
                        st.markdown(f"""
                        <div class="metric-card">
                            <strong>#{i} {bigram}</strong> {score_color}<br>
                            📊 {count} occurrences | ⭐ Importance: {score}/10
                        </div>
                        """, unsafe_allow_html=True)

            with tab3:
                # Top Resume Keywords
                st.markdown("### 📝 **Top Keywords in Your Resume**")
                if match_results["top_resume_keywords"]:
                    for i, (word, count, score) in enumerate(match_results["top_resume_keywords"], 1):
                        score_color = "🟢" if score >= 8 else "🟡" if score >= 6 else "🔴"
                        st.markdown(f"""
                        <div class="metric-card">
                            <strong>#{i} {word}</strong> {score_color}<br>
                            📊 {count} occurrences | ⭐ Importance: {score}/10
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="warning-card">⚠ No significant keywords found in resume.</div>', unsafe_allow_html=True)

                # Top Resume Bigrams
                st.markdown("### 📝 **Top Phrases in Your Resume**")
                if match_results["top_resume_bigrams"]:
                    for i, (bigram, count, score) in enumerate(match_results["top_resume_bigrams"], 1):
                        score_color = "🟢" if score >= 8 else "🟡" if score >= 6 else "🔴"
                        st.markdown(f"""
                        <div class="metric-card">
                            <strong>#{i} {bigram}</strong> {score_color}<br>
                            📊 {count} occurrences | ⭐ Importance: {score}/10
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="warning-card">⚠ No significant phrases found in resume.</div>', unsafe_allow_html=True)

                # Keyword Matches
                st.markdown("### ✅ **Keyword Matches in Your Resume**")
                if match_results["keyword_matches"]:
                    for word, job_count in match_results["keyword_matches"]:
                        st.markdown(f"""
                        <div class="success-card">
                            ✔ <strong>{word}</strong>: {job_count} occurrences in job posting
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="warning-card">⚠ No keyword matches found.</div>', unsafe_allow_html=True)

                # Bigram Matches
                st.markdown("### 🔗 **Phrase Matches in Your Resume**")
                if match_results["bigram_matches"]:
                    for bigram, job_count in match_results["bigram_matches"]:
                        st.markdown(f"""
                        <div class="success-card">
                            ✔ <strong>{bigram}</strong>: {job_count} occurrences in job posting
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="warning-card">⚠ No phrase matches found.</div>', unsafe_allow_html=True)

            with tab4:
                st.markdown("### ⚠️ **Optimization Opportunities**")
                
                improvement_found = False
                
                # Missing Important Keywords
                if match_results["missing_keywords"]:
                    improvement_found = True
                    st.markdown("#### ❌ **Missing Important Keywords**")
                    st.markdown("Consider adding these keywords to your resume:")
                    
                    # Create chips for missing keywords
                    keyword_chips = ""
                    for keyword in match_results["missing_keywords"]:
                        keyword_chips += f'<span style="background:#34495e;color:white;padding:4px 8px;margin:2px;border-radius:12px;font-size:12px;">{keyword}</span> '
                    
                    st.markdown(f'<div style="margin:10px 0;">{keyword_chips}</div>', unsafe_allow_html=True)

                # Missing Important Bigrams
                if match_results["missing_bigrams"]:
                    improvement_found = True
                    st.markdown("#### ❌ **Missing Important Phrases**")
                    st.markdown("Consider incorporating these phrases into your resume:")
                    
                    # Create chips for missing bigrams
                    bigram_chips = ""
                    for bigram in match_results["missing_bigrams"]:
                        bigram_chips += f'<span style="background:#3498db;color:white;padding:4px 8px;margin:2px;border-radius:12px;font-size:12px;">{bigram}</span> '
                    
                    st.markdown(f'<div style="margin:10px 0;">{bigram_chips}</div>', unsafe_allow_html=True)
                
                if not improvement_found:
                    st.success("🎉 Great job! Your resume includes all the important keywords and phrases from the job posting.")
                    st.balloons()

            # Add some helpful tips at the bottom
            st.markdown("---")
            st.markdown("### 💡 **Optimization Tips**")
            
            tip_col1, tip_col2, tip_col3 = st.columns(3)
            
            with tip_col1:
                st.markdown("""
                <div class="metric-card">
                    <h4>🎯 Keywords</h4>
                    <p>Use exact keywords from the job posting. Avoid synonyms where possible.</p>
                </div>
                """, unsafe_allow_html=True)
            
            with tip_col2:
                st.markdown("""
                <div class="metric-card">
                    <h4>🔗 Context</h4>
                    <p>Include keywords in meaningful phrases that demonstrate your experience.</p>
                </div>
                """, unsafe_allow_html=True)
            
            with tip_col3:
                st.markdown("""
                <div class="metric-card">
                    <h4>📊 Balance</h4>
                    <p>Don't overuse keywords. Maintain natural, readable content.</p>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #64748b; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 10px; margin-top: 2rem; border: 1px solid #cbd5e1;">
    <p>📄 <strong style="color: #2c3e50;">Resume Analyzer</strong> | Powered by Advanced Text Processing</p>
    <p><small>💡 Tip: Run this analysis multiple times as you refine your resume for better results</small></p>
</div>
""", unsafe_allow_html=True)
