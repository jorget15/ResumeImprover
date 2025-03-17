import docx2txt
import PyPDF2
from collections import Counter
import re
from nltk import bigrams
from analyzer import load_excluded_words, lemmatize_word, calculate_importance


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    return docx2txt.process(file_path)


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    PDFtext = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            PDFtext += page.extract_text() + "\n"
    return PDFtext

def extract_text(file_path):
    """Extract text from a DOCX or PDF file."""
    if file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
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
    return "[WIP] Automatic job posting extraction from URLs is under development. Please paste the job description manually."

def extract_keywords(text, excluded_words_path="excluded_words.json", top_n=5):
    """Finds the most frequent words (ignoring single occurrences), assigns importance scores, and returns occurrence count."""
    excluded_words = load_excluded_words(excluded_words_path)  # Load excluded words
    words = re.findall(r"\b\w+\b", text.lower())  # Tokenize words
    filtered_words = [lemmatize_word(word) for word in words if word not in excluded_words]

    word_counts = Counter(filtered_words)
    importance_scores = calculate_importance(word_counts)

    return [(word, count, importance_scores[word]) for word, count in word_counts.most_common(top_n) if count > 1]

def extract_bigrams(text, excluded_words_path="excluded_words.json", top_n=5):
    """Extracts properly formatted bigrams, excluding single occurrences."""
    excluded_words = load_excluded_words(excluded_words_path)
    words = re.findall(r"\b\w+\b", text.lower())
    filtered_words = [lemmatize_word(word) for word in words if word not in excluded_words]

    # Ensure bigrams() receives a list of words, not a single string
    bigram_pairs = list(bigrams(filtered_words))
    bigram_counts = Counter(bigram_pairs)
    importance_scores = calculate_importance(bigram_counts)

    # Properly join bigrams for output
    return [(" ".join(pair), count, importance_scores[pair])
            for pair, count in bigram_counts.most_common(top_n) if count > 1]
