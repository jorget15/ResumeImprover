import re
from extractor import extract_keywords, extract_bigrams

def analyze_resume_against_job(resume_text, job_text, company_name=None):
    """
    Finds top job posting keywords/bigrams, compares them to ALL resume keywords/bigrams.
    Also extracts top 5 from resume for display in UI.
    """
    # 1) Job
    job_keywords = extract_keywords(job_text, top_n=5, company_name=company_name)
    job_bigrams = extract_bigrams(job_text, top_n=5, company_name=company_name)

    # 2) Resume (ALL)
    resume_keywords_all = extract_keywords(resume_text, top_n=None, company_name=company_name)
    resume_bigrams_all = extract_bigrams(resume_text, top_n=None, company_name=company_name)

    # 3) Resume (TOP 5) - for display
    resume_keywords_top = resume_keywords_all[:5]
    resume_bigrams_top = resume_bigrams_all[:5]

    # 4) Identify matches & missing elements
    # job_keywords => [(word, job_count, job_score), ...]
    # resume_keywords_all => [(word, res_count, res_score), ...]

    # Match if job_word == res_word
    keyword_matches = [
        (word, job_count)
        for (word, job_count, _) in job_keywords
        if word in [rword for (rword, _, _) in resume_keywords_all]
    ]
    bigram_matches = [
        (bigram, job_count)
        for (bigram, job_count, _) in job_bigrams
        if bigram in [rbg for (rbg, _, _) in resume_bigrams_all]
    ]

    missing_keywords = [
        word for (word, _, _) in job_keywords
        if word not in [rword for (rword, _, _) in resume_keywords_all]
    ]
    missing_bigrams = [
        bigram for (bigram, _, _) in job_bigrams
        if bigram not in [rbg for (rbg, _, _) in resume_bigrams_all]
    ]

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
