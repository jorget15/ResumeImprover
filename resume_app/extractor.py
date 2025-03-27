import re
import pdfplumber
import docx2txt
import nltk
import unicodedata
from collections import Counter

from analyzer import (
    load_excluded_words,
    lemmatize_word,
    calculate_importance,
    normalize_token,  # We can import the normalizer from analyzer
)

def extract_resume_text(uploaded_file):
    """Extracts text from a PDF or DOCX resume uploaded via Streamlit."""
    if not uploaded_file:
        return ""

    file_type = uploaded_file.type
    if file_type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(uploaded_file)

    return ""

def extract_text_from_paste(pasted_text):
    """
    Returns the pasted text or a default message if empty.
    Could be used for job description input in Streamlit.
    """
    if pasted_text.strip():
        return pasted_text.strip()
    else:
        return "No job description provided."

def extract_keywords(text, top_n=5, company_name=None):
    """
    Finds frequent words while ignoring excluded words. Returns a list of (word, count, importance).
    If top_n is None, returns all words with freq>1.
    """
    excluded_words = load_excluded_words(company_name)
    # Tokenize
    raw_tokens = re.findall(r"\b\w+\b", text.lower())
    # Normalize & Filter
    normalized_tokens = [normalize_token(tok) for tok in raw_tokens]
    filtered = [lemmatize_word(tok) for tok in normalized_tokens if tok not in excluded_words]

    word_counts = Counter(filtered)
    importance_scores = calculate_importance(word_counts)

    if top_n is not None:
        # Return top_n words (count>1) with importance
        return [
            (w, c, importance_scores[w])
            for w, c in word_counts.most_common(top_n)
            if c > 1
        ]
    else:
        # Return ALL words with freq>1
        return [
            (w, c, importance_scores[w])
            for w, c in word_counts.most_common()
            if c > 1
        ]

def extract_bigrams(text, top_n=5, company_name=None):
    """
    Finds most frequent bigrams. Filters out any bigrams containing excluded words.
    Returns list of (bigram, count, importance).
    """
    excluded_words = load_excluded_words(company_name)
    raw_tokens = re.findall(r"\b\w+\b", text.lower())
    normalized_tokens = [normalize_token(tok) for tok in raw_tokens]
    lemma_tokens = [lemmatize_word(tok) for tok in normalized_tokens if tok not in excluded_words]

    # Generate bigrams from filtered tokens
    bigrams_list = list(nltk.bigrams(lemma_tokens))
    # Optionally filter out bigrams that contain excluded words
    bigrams_list = [
        bg for bg in bigrams_list
        if not any(word in excluded_words for word in bg)
    ]

    bigram_strs = [" ".join(bg) for bg in bigrams_list]
    bigram_counts = Counter(bigram_strs)
    importance_scores = calculate_importance(bigram_counts)

    if top_n is not None:
        return [
            (bg, cnt, importance_scores[bg])
            for bg, cnt in bigram_counts.most_common(top_n)
            if cnt > 1
        ]
    else:
        return [
            (bg, cnt, importance_scores[bg])
            for bg, cnt in bigram_counts.most_common()
            if cnt > 1
        ]
