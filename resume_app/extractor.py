import nltk
import pdfplumber
import docx2txt
from collections import Counter
import re
from analyzer import load_excluded_words, lemmatize_word, calculate_importance
import unicodedata


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


# def extract_text_from_url(url):
#    """Placeholder function for future API integration. Displays WIP message."""
#    return ("[WIP] Automatic job posting extraction from URLs is under development. "
#            "Please paste the job description manually.")


def extract_keywords(text, top_n=5, company_name=None):
    """Finds the most frequent words (ignoring single occurrences), assigns importance scores."""

    excluded_words = load_excluded_words(company_name)
    words = re.findall(r"\b\w+\b", text.lower())

    # Normalize each raw token
    normalized_words = [normalize_token(w) for w in words]

    # Filter out excluded words, then lemmatize
    filtered_words = []
    for token in normalized_words:
        if token not in excluded_words:
            filtered_words.append(lemmatize_word(token))

    word_counts = Counter(filtered_words)
    importance_scores = calculate_importance(word_counts)

    if top_n is not None:
        return [
            (word, count, importance_scores[word])
            for word, count in word_counts.most_common(top_n)
            if count > 1
        ]
    else:
        return [
            (word, count, importance_scores[word])
            for word, count in word_counts.most_common()
            if count > 1
        ]

def extract_bigrams(text, company_name=None, top_n=5):
    """Finds the most frequent bigrams while removing excluded words."""
    excluded_words = load_excluded_words(company_name)  # ✅ Load excluded words
    words = re.findall(r"\b\w+\b", text.lower())  # ✅ Convert words to lowercase
    filtered_words = [lemmatize_word(word) for word in words if word not in excluded_words]

    bigrams = list(nltk.bigrams(filtered_words))  # ✅ Generate bigrams from filtered words
    filtered_bigrams = [" ".join(bigram) for bigram in bigrams if not any(word in excluded_words for word in bigram)]
    bigram_counts = Counter([" ".join(bigram) for bigram in bigrams])  # ✅ Join words into bigrams

    importance_scores = calculate_importance(bigram_counts)

    return [(bigram, count, importance_scores[bigram]) for bigram, count in bigram_counts.most_common(top_n) if
            count > 1]


def normalize_token(token: str) -> str:
    """
    Convert to a normalized form and strip any hidden whitespace/unicode.
    """
    # Normalize to NFKC to unify visually identical but distinct codepoints
    token = unicodedata.normalize("NFKC", token)
    # Strip all whitespace (including zero-width spaces)
    token = token.strip()
    return token
