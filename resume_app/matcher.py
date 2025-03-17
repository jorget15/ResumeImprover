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

    # Convert keyword tuples to lists
    job_keyword_list = [word for word, _, _ in job_keywords]
    job_bigram_list = [bigram for bigram, _, _ in job_bigrams]

    resume_keyword_list = [word for word, _, _ in resume_keywords]
    resume_bigram_list = [bigram for bigram, _, _ in resume_bigrams]

    # Debugging: Print extracted bigrams before matching
    print("\n🔍 Debugging Extracted Job Posting Bigrams:")
    print(job_bigram_list)

    print("\n🔍 Debugging Extracted Resume Bigrams:")
    print(resume_bigram_list)

    # Count occurrences of job keywords in the resume
    keyword_matches = count_matches(resume_text, job_keyword_list)
    bigram_matches = count_matches(resume_text, job_bigram_list)

    # Identify missing but important job posting keywords
    missing_keywords = [word for word in job_keyword_list if keyword_matches[word] == 0]
    missing_bigrams = [bigram for bigram in job_bigram_list if bigram_matches[bigram] == 0]

    return {
        "keyword_matches": keyword_matches,
        "bigram_matches": bigram_matches,
        "missing_keywords": missing_keywords,
        "missing_bigrams": missing_bigrams
    }
