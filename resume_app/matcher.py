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

def analyze_resume_against_job(resume_text, job_text):
    """Finds keyword & bigram matches between the resume and job description."""

    excluded_words = load_excluded_words()

    # Extract job posting keywords and bigrams
    job_keywords = extract_keywords(job_text)
    job_bigrams = extract_bigrams(job_text)

    # Extract resume keywords and bigrams
    resume_keywords = extract_keywords(resume_text)
    resume_bigrams = extract_bigrams(resume_text)

    # Convert to sets for easy matching
    job_keyword_set = {word for word, _, _ in job_keywords}
    job_bigram_set = {bigram for bigram, _, _ in job_bigrams}
    resume_keyword_set = {word for word, _, _ in resume_keywords}
    resume_bigram_set = {bigram for bigram, _, _ in resume_bigrams}

    # Find matches
    keyword_matches = [(word, count) for word, count, _ in job_keywords if word in resume_keyword_set]
    bigram_matches = [(bigram, count) for bigram, count, _ in job_bigrams if bigram in resume_bigram_set]

    # Find missing important keywords & bigrams
    missing_keywords = [word for word in job_keyword_set if word not in resume_keyword_set]
    missing_bigrams = [bigram for bigram in job_bigram_set if bigram not in resume_bigram_set]

    return {
        "top_job_keywords": job_keywords,  # List of all job posting keywords
        "top_job_bigrams": job_bigrams,    # List of all job posting bigrams
        "keyword_matches": keyword_matches,
        "bigram_matches": bigram_matches,
        "missing_keywords": missing_keywords,
        "missing_bigrams": missing_bigrams
    }

