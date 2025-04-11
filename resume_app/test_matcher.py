import re
import unicodedata

from analyzer import load_excluded_words, lemmatize_word  # Adjust imports as needed
from extractor import extract_keywords, extract_bigrams

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


def normalize_token(token: str) -> str:
    """
    Convert token to a normalized form and strip hidden whitespace/unicode
    so that 'a ' or 'a\u00a0' becomes 'a'.
    """
    # Normalize to NFKC to unify different but similar Unicode codepoints
    token = unicodedata.normalize("NFKC", token)
    # Strip trailing spaces, zero-width spaces, etc.
    return token.strip()


def debug_exclusion(company_name=None):
    """Debug function to see how excluded words filter out 'a' or any other tokens."""

    # 1) Load excluded words
    excluded_words = load_excluded_words(company_name)
    print("Excluded words:", excluded_words)

    if "a" in excluded_words:
        print("'a' is in excluded_words!")
    else:
        print("'a' is NOT in excluded_words...")

    # 2) Regex tokenize (in lowercase)
    raw_tokens = re.findall(r"\b\w+\b", job_text.lower())

    # 2a) Print the first 30 raw tokens with repr()
    print("\n--- First 30 raw tokens (repr) ---")
    for i, t in enumerate(raw_tokens[:30]):
        print(i, repr(t))

    # 3) Normalize each token
    normalized_tokens = [normalize_token(token) for token in raw_tokens]

    # 3a) Print the first 30 normalized tokens with repr()
    print("\n--- First 30 normalized tokens (repr) ---")
    for i, t in enumerate(normalized_tokens[:30]):
        print(i, repr(t))

    # 4) Lemmatize each normalized token
    lemmatized_tokens = [lemmatize_word(w) for w in normalized_tokens]
    print("\n--- First 30 lemmatized tokens ---")
    print(lemmatized_tokens[:30])

    # 5) Filter out excluded words AFTER normalization
    filtered_tokens = [lemmatize_word(w) for w in normalized_tokens if w not in excluded_words]

    # 5a) Print the first 30 filtered tokens
    print("\n--- First 30 filtered tokens ---")
    print(filtered_tokens[:30])

    # 5b) Check if 'a' is still in filtered tokens
    if "a" in filtered_tokens:
        print("\n*** 'a' is STILL in filtered_tokens ***")
    else:
        print("\n'a' is not in filtered_tokens, which is correct!")

    # 6) Show top 10 job keywords
    print("\n--- Top 10 Job Keywords ---")
    top_keywords = extract_keywords(job_text, top_n=10, company_name=company_name)
    for kw, count, score in top_keywords:
        print(f"{kw}: {count} occurrences, importance {score}/10")

    print("\n--- Checking each normalized token for 'a' ---")
    for i, tok in enumerate(normalized_tokens):
        if tok == "a":
            print(f"Token index {i} is 'a', excluded? {tok in excluded_words}")

    for i, token in enumerate(normalized_tokens):
        print(i, repr(token))


if __name__ == "__main__":
    debug_exclusion(company_name=None)  # or "FBI", "A", etc. to test
