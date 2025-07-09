# 📄 Resume vs Job Posting Analyzer

> **Optimize your resume to match job requirements perfectly and bypass ATS systems**

A powerful Streamlit-based web application that analyzes the alignment between your resume and job postings using advanced text processing techniques. Get detailed insights on keyword matches, missing terms, and optimization recommendations to improve your chances of landing interviews.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.43.2-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **📊 Smart Analysis**: Advanced text processing to identify critical keywords and phrases
- **🎯 Match Scoring**: Get an overall match percentage between your resume and job requirements
- **🔍 Keyword Intelligence**: Discover top keywords in job postings with importance scores
- **📝 Resume Optimization**: See exactly which terms are missing from your resume
- **🏢 Company Filtering**: Exclude company-specific terms from analysis for better accuracy
- **📱 Modern UI**: Beautiful, responsive interface with intuitive tabs and visual feedback
- **📈 Visual Insights**: Color-coded importance levels and progress indicators

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resume-improver.git
   cd resume-improver
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd resume_app
   pip install -r requirements.txt
   ```

4. **Download NLTK data** (first time only)
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

5. **Run the application**
   ```bash
   streamlit run "Streamlit UI.py"
   ```

6. **Open your browser** and go to `http://localhost:8501`

## 📖 How to Use

### Step 1: Enter Company Information
- Input the company name to filter out company-specific terms from analysis

### Step 2: Upload Your Resume
- Support for **PDF** and **DOCX** formats
- Get a preview of extracted text to verify accuracy

### Step 3: Paste Job Posting
- Copy and paste the complete job description
- Include requirements, responsibilities, and qualifications

### Step 4: Analyze & Optimize
- Click "Analyze Resume" to get comprehensive insights
- Review results across four organized tabs:
  - **📊 Overview**: Match score and key metrics
  - **🔍 Job Keywords**: Important terms from the job posting
  - **📝 Resume Analysis**: Keywords found in your resume
  - **❌ Missing Elements**: Optimization opportunities

## 🎯 Understanding Results

### Importance Scoring
- **🟢 8-10**: Critical keywords - must include
- **🟡 6-7**: Important keywords - should include  
- **🔴 1-5**: Nice to have keywords

### Match Score
- **80%+**: Excellent match - resume aligns very well
- **60-79%**: Good match - minor improvements needed
- **40-59%**: Moderate match - significant improvements recommended
- **<40%**: Low match - major revision needed

## 🛠️ Technical Architecture

### Core Components

- **`extractor.py`**: Document text extraction (PDF/DOCX)
- **`analyzer.py`**: Text preprocessing and keyword scoring
- **`matcher.py`**: Resume-job posting comparison logic
- **`Streamlit UI.py`**: Web interface and user experience
- **`excluded_words.json`**: Stop words and common terms filter

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.43.2 | Web application framework |
| pdfplumber | 0.11.5 | PDF text extraction |
| python-docx | 1.1.2 | DOCX document processing |
| nltk | 3.9.1 | Natural language processing |
| numpy | 2.2.3 | Numerical computations |
| requests | 2.32.3 | HTTP requests |
| beautifulsoup4 | 4.13.4 | Web scraping capabilities |

## 📁 Project Structure

```
resume-improver/
├── resume_app/
│   ├── Streamlit UI.py      # Main web application
│   ├── analyzer.py          # Text analysis engine
│   ├── extractor.py         # Document processing
│   ├── matcher.py           # Matching algorithms
│   ├── test_matcher.py      # Unit tests
│   ├── excluded_words.json  # Stop words configuration
│   ├── requirements.txt     # Python dependencies
│   ├── resumes/            # Sample resume storage
│   └── __pycache__/        # Python cache files
└── README.md               # Project documentation
```

## 🧪 Testing

Run the included tests to verify functionality:

```bash
python -m pytest test_matcher.py -v
```

## 🔧 Configuration

### Excluded Words
Customize `excluded_words.json` to add domain-specific stop words or company names that should be filtered out during analysis.

### Scoring Algorithm
The importance scoring combines:
- **Term Frequency**: How often keywords appear
- **Position Weight**: Earlier mentions score higher
- **Context Analysis**: Surrounding word importance
- **Industry Relevance**: Domain-specific term recognition

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Tips for Best Results

- **Use exact keywords** from job postings rather than synonyms
- **Include keywords in context** rather than just listing them
- **Focus on high-importance keywords** (8+ score) first
- **Maintain natural, readable content** - avoid keyword stuffing
- **Run analysis multiple times** as you refine your resume

## 🐛 Troubleshooting

### Common Issues

**Import Errors**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

**NLTK Data Missing**: Download required data
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

**File Upload Issues**: Verify file format (PDF/DOCX only) and size (<200MB)

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the documentation

---

**Made with ❤️ to help job seekers optimize their resumes and land their dream jobs!**
