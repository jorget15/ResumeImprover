import re
from analyzer import load_excluded_words, lemmatize_word  # Make sure these are correct imports
from extractor import extract_keywords, extract_bigrams

# Example job_text you want to debug:
job_text = """
This role serves as a technical subject matter expert by actively participating in
configuration consultation, vendor evaluation, and problem resolution of multiple
Microsoft systems. The candidate should have a clear understanding of how to research,
design, implement, and troubleshoot Microsoft information systems, cloud technologies,
and technology solutions in support of business needs. Under limited supervision, the
candidate will effectively manage and prioritize assigned projects and design complex
multi-system solutions to meet the organization's needs. Recommendations in these
areas should be made with a high level of technical competency.
"""

def debug_exclusion(company_name=None):
    """Debug function to see how excluded words filter out 'a' or any other tokens."""

    # 1️⃣ Load excluded words
    excluded_words = load_excluded_words(company_name)
    print("Excluded words:", excluded_words)

    if "a" in excluded_words:
        print("'a' is in excluded_words!")
    else:
        print("'a' is NOT in excluded_words...")

    # 2️⃣ Tokenize text
    words = re.findall(r"\b\w+\b", job_text.lower())
    print("\n--- First 30 tokens in job_text ---")
    print(words[:30])

    # 3️⃣ Show lemmatization & identify if 'a' remains
    lemmatized_tokens = [lemmatize_word(w) for w in words]
    print("\n--- First 30 lemmatized tokens ---")
    print(lemmatized_tokens[:30])

    # 4️⃣ Filter out excluded words
    filtered_tokens = [lemmatize_word(w) for w in words if w not in excluded_words]
    print("\n--- First 30 filtered tokens ---")
    print(filtered_tokens[:30])

    # 5️⃣ Optionally show the top 10 keywords
    top_keywords = extract_keywords(job_text, top_n=10, company_name=company_name)
    print("\n--- Top 10 Job Keywords ---")
    for kw, count, score in top_keywords:
        print(f"{kw}: {count} occurrences, importance {score}/10")

# Run the debug function
if __name__ == "__main__":
    debug_exclusion(company_name=None)  # or "FBI" or whatever
