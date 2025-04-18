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
    normalize_token,
)


def extract_resume_text(uploaded_file):
    """Extracts text from a PDF or DOCX resume uploaded via Streamlit."""
    if not uploaded_file:
        return "" #if no file is provided return empty string

    file_type = uploaded_file.type
    if file_type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages) #return all lines as a single text
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(uploaded_file)  #Return all lines as a single text

    return "" #if not DOCX or PDF return empty string


def extract_text_from_paste(pasted_text):
    """
    Handles the user input regarding the job posting
    """
    if pasted_text.strip():
        return pasted_text.strip()
    else:
        return "No job description provided."


def extract_keywords(text, top_n=5, company_name=None):
    """
    Identify top `top_n` keywords (words with count > 1), excluding stop/excluded words.
    Returns list of (word, count, importance_score).
    If top_n is None, returns all words with freq > 1.
    """
    if company_name:
        text = text.replace(company_name, "")  # Remove full company name from job posting text
        abbreviation = ''.join([w[0] for w in company_name.lower().split()])
        text = text.replace(abbreviation, "")          # Also remove abbreviation manually

    excluded_words = load_excluded_words(company_name) #load list of common irrelevant words
    # Tokenize and convert to lowercase to standardize
    raw_tokens = re.findall(r"\b\w+\b", text.lower())
    # Normalize tokens
    normalized_tokens = [normalize_token(tok) for tok in raw_tokens]
    #Lemmatize tokens (make them become their base form)
    filtered = [lemmatize_word(tok) for tok in normalized_tokens if tok.lower() not in excluded_words]

    word_counts = Counter(filtered) #count word/token frequencies after filtering them
    importance_scores = calculate_importance(word_counts) #make them fit a scale of 1-10

    if top_n is not None:
        # Return top `top_n` items with count > 1
        return [
            (w, c, importance_scores[w])
            for w, c in word_counts.most_common(top_n)
            if c > 1
        ]
    else:
        # Return all items with freq > 1
        return [
            (w, c, importance_scores[w])
            for w, c in word_counts.most_common()
            if c > 1
        ]


def extract_bigrams(text, top_n=5, company_name=None):
    """
    Identify top `top_n` bigrams (2-word sequences), excluding any that contain excluded words.
    Returns list of ("word1 word2", count, importance_score).
    If top_n is None, returns all bigrams with freq > 1.
    """
    excluded_words = load_excluded_words(company_name) #get excluded words list + company name
    raw_tokens = re.findall(r"\b\w+\b", text.lower())
    normalized_tokens = [normalize_token(tok) for tok in raw_tokens]
    lemma_tokens = [lemmatize_word(tok) for tok in normalized_tokens if tok not in excluded_words] #lemmatize and filter tokens

    # Generate bigrams from filtered tokens
    bigrams_list = list(nltk.bigrams(lemma_tokens))
    # Filter out any bigram containing excluded terms
    bigrams_list = [
        bg for bg in bigrams_list
        if not any(word in excluded_words for word in bg)
    ]

    # Convert bigram to string "w1 w2"
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
