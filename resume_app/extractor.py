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
    """Finds frequent words while removing excluded words + normalization."""
    excluded_words = load_excluded_words(company_name)
    # 1) Tokenize raw text in lowercase
    raw_tokens = re.findall(r"\b\w+\b", text.lower())
    # 2) Normalize each token
    def normalize_token(tok):
        # Turn to NFKC
        tok = unicodedata.normalize("NFKC", tok)
        tok = tok.strip()
        return tok

    normalized_tokens = [normalize_token(t) for t in raw_tokens]
    # 3) Filter out excluded words, lemmatize
    filtered_tokens = []
    for tok in normalized_tokens:
        if tok not in excluded_words:
            filtered_tokens.append(lemmatize_word(tok))

    # 4) Count frequencies + importance
    word_counts = Counter(filtered_tokens)
    importance = calculate_importance(word_counts)

    # 5) Return top_n or all
    if top_n is not None:
        return [(w, c, importance[w]) for w, c in word_counts.most_common(top_n) if c > 1]
    else:
        return [(w, c, importance[w]) for w, c in word_counts.most_common() if c > 1]

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
