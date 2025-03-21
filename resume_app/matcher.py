from extractor import extract_keywords, extract_bigrams  # Import from extractor now
from analyzer import load_excluded_words  # Load excluded words from analyzer
import re
from collections import defaultdict


def count_matches(text, keywords):
    """Counts occurrences of job-related keywords and bigrams in a resume."""
    word_counts = defaultdict(int)

    for keyword in keywords:
        # Escape special regex characters in keyword/bigram
        pattern = re.escape(keyword)
        # Count exact occurrences using regex word boundaries
        matches = re.findall(r'\b' + pattern + r'\b', text.lower())
        word_counts[keyword] = len(matches)

    return word_counts


def analyze_resume_against_job(resume_text, job_text, company_name=None):
    """Finds keyword & bigram matches between the resume and job posting."""

    # Extract job keywords & bigrams
    job_keywords = extract_keywords(job_text, top_n=5, company_name=company_name)
    job_bigrams = extract_bigrams(job_text, top_n=5, company_name=company_name)

    # Extract ALL resume keywords & bigrams
    resume_keywords_all = extract_keywords(resume_text, top_n=None, company_name=company_name)  # Extract ALL keywords
    resume_bigrams_all = extract_bigrams(resume_text, top_n=None, company_name=company_name)  # Extract ALL bigrams

    # Extract TOP resume keywords & bigrams for UI display
    resume_keywords_top = resume_keywords_all[:5]  # Keep top 5 for display
    resume_bigrams_top = resume_bigrams_all[:5]

    # Identify matches
    keyword_matches = [(word, count) for word, count, _ in job_keywords if word in [kw[0] for kw in resume_keywords_all]]
    bigram_matches = [(bigram, count) for bigram, count, _ in job_bigrams if bigram in [bg[0] for bg in resume_bigrams_all]]

    # Identify missing elements
    missing_keywords = [word for word, _, _ in job_keywords if word not in [kw[0] for kw in resume_keywords_all]]
    missing_bigrams = [bigram for bigram, _, _ in job_bigrams if bigram not in [bg[0] for bg in resume_bigrams_all]]

    return {
        "top_job_keywords": job_keywords,
        "top_job_bigrams": job_bigrams,
        "top_resume_keywords": resume_keywords_top,
        "top_resume_bigrams": resume_bigrams_top,
        "keyword_matches": keyword_matches,
        "bigram_matches": bigram_matches,
        "missing_keywords": missing_keywords,
        "missing_bigrams": missing_bigrams,
    }

