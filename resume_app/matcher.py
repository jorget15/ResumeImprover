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

    excluded_words = load_excluded_words(company_name)  # Exclude only the company name

    # Extract job keywords & bigrams
    job_keywords = extract_keywords(job_text, top_n=5, company_name=company_name)
    job_bigrams = extract_bigrams(job_text, top_n=5, company_name=company_name)

    # Extract resume keywords & bigrams
    resume_keywords = extract_keywords(resume_text, top_n=5, company_name=None)
    resume_bigrams = extract_bigrams(resume_text, top_n=5, company_name=None)

    # Identify matches & missing elements
    keyword_matches = [(word, resume_keywords[word]) for word in job_keywords if word in resume_keywords]
    bigram_matches = [(bigram, resume_bigrams[bigram]) for bigram in job_bigrams if bigram in resume_bigrams]

    missing_keywords = [word for word in job_keywords if word not in resume_keywords]
    missing_bigrams = [bigram for bigram in job_bigrams if bigram not in resume_bigrams]

    return {
        "top_job_keywords": job_keywords,  # Remove .items()
        "top_job_bigrams": job_bigrams,  # Remove .items()
        "keyword_matches": keyword_matches,
        "bigram_matches": bigram_matches,
    }
