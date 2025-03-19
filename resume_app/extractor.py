import pdfplumber
import docx2txt
from collections import Counter
import re
from nltk import bigrams
from analyzer import load_excluded_words, lemmatize_word, calculate_importance


def extract_resume_text(uploaded_file):
    """Extracts text from a PDF or DOCX resume."""
    if uploaded_file is None:
        return ""

    file_type = uploaded_file.type

    if file_type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(uploaded_file)

    return ""


def extract_text(file_path):
    """Extract text from a DOCX or PDF file."""
    if file_path.lower().endswith(".docx"):
        return extract_resume_text(file_path)
    elif file_path.lower().endswith(".pdf"):
        return extract_resume_text(file_path)
    else:
        raise ValueError("Unsupported file format. Please use DOCX or PDF.")


def extract_text_from_paste(pasted_text):
    """Returns the pasted job description text."""
    if pasted_text.strip():
        return pasted_text.strip()
    else:
        return "No job description provided. Please paste the job description."


def extract_text_from_url(url):
    """Placeholder function for future API integration. Displays WIP message."""
    return ("[WIP] Automatic job posting extraction from URLs is under development. "
            "Please paste the job description manually.")


def extract_keywords(text, excluded_words_path="excluded_words.json", top_n=5, company_name=None):
    """Finds the most frequent words (ignoring single occurrences), assigns importance scores, and returns occurrence count."""
    excluded_words = load_excluded_words(company_name)  # Load excluded words
    words = re.findall(r"\b\w+\b", text.lower())  # Tokenize words
    filtered_words = [lemmatize_word(word) for word in words if word not in excluded_words]

    word_counts = Counter(filtered_words)
    importance_scores = calculate_importance(word_counts)

    return [(word, count, importance_scores[word]) for word, count in word_counts.most_common(top_n) if count > 1]


def extract_bigrams(text, top_n=5, company_name=None):
    """Extracts properly formatted bigrams, excluding single occurrences."""
    excluded_words = load_excluded_words(company_name)
    words = re.findall(r"\b\w+\b", text.lower())
    filtered_words = [lemmatize_word(word) for word in words if word not in excluded_words]

    # Ensure bigrams() receives a list of words, not a single string
    bigram_pairs = list(bigrams(filtered_words))
    bigram_counts = Counter(bigram_pairs)
    importance_scores = calculate_importance(bigram_counts)

    # Properly join bigrams for output
    return [(" ".join(pair), count, importance_scores[pair])
            for pair, count in bigram_counts.most_common(top_n) if count > 1]


def extract_company_name(text):
    """Extracts the company name from job postings using patterns."""
    patterns = [
        r"([A-Za-z\s]+) is looking for",  # Example: "Google is looking for..."
        r"([A-Za-z\s]+) seeks",  # Example: "Amazon seeks a..."
        r"at ([A-Za-z\s]+)"  # Example: "Software Engineer at Microsoft"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()

    return "Unknown Company"
