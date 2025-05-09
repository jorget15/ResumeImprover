import json
import os
import re
import nltk
import nltk.data
import unicodedata
from nltk import WordNetLemmatizer, pos_tag
from nltk.corpus import wordnet

# Force NLTK download on both local and Streamlit Cloud
nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data")
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)
nltk.data.path.append(nltk_data_path)

# List of required NLTK resources
nltk_resources = [
    "averaged_perceptron_tagger_eng",
    "wordnet",
    "omw-1.4"
    # "averaged_perceptron_tagger_eng" alternative tagger
]


def ensure_nltk_resources():
    """Ensure all required NLTK models are installed."""
    for resource in nltk_resources:
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(resource.split('/')[-1], download_dir=nltk_data_path)


# Initialize NLTK resources at import
ensure_nltk_resources()

print("✅ NLTK is now using this path:", nltk.data.path)  # Debug print

''' I had a lot of issues with these resources. '''


def expand_company_terms(company_name: str):
    """Break company name into parts, abbreviation, and full string."""
    parts = company_name.lower().split()
    abbrev = ''.join([w[0] for w in parts if w])
    terms = set(parts)
    terms.add(abbrev)
    terms.add(company_name.lower())
    return terms


def load_excluded_words(company_name=None):
    """
    Loads excluded words from excluded_words.json. Appends
    company name and its variants (abbreviation + individual words).
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excluded_path = os.path.join(script_dir, "excluded_words.json")

    excluded_words = set()

    # Load all categories from excluded_words.json
    if os.path.exists(excluded_path):
        with open(excluded_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for category_values in data.values():
                if isinstance(category_values, list):
                    for word in category_values:
                        if isinstance(word, list):
                            # Flatten nested lists
                            excluded_words.update(w.lower().strip() for w in word)
                        else:
                            excluded_words.add(word.lower().strip())

    # Exclude company name variants if provided
    if company_name and company_name.strip():
        excluded_words |= expand_company_terms(company_name.strip())
        print("❗ Final excluded words sample:", sorted(list(excluded_words))[:20])  # Debug Print

    return excluded_words


# use WordNet's Lemmatizer object (changes "running" to "run")
lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(word):
    """Map Part of Speech (POS) tag to first character WordNetLemmatizer understands."""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)  # Default to NOUN for unknown


def lemmatize_word(word):
    """
    Lemmatizes a single token. Also handles some manual special cases:
    e.g., 'engineering' -> 'engineer', 'programming' -> 'program'.
    """
    lemma = lemmatizer.lemmatize(word.lower(), get_wordnet_pos(
        word))  # ensures word is lowercase, lets the lemmatizer know what POS is working with
    special_cases = {
        "engineering": "engineer",
        "programming": "program",
        "developing": "develop",
        "analyzing": "analyze",
    }  # Some words that usually do not get lemmatized
    return special_cases.get(lemma, lemma)


def calculate_importance(counts):
    """
    Assigns importance scores from 1 to 10. The highest-count word gets 10,
    scaling down proportionally for others.
    """
    if not counts:
        return {}

    max_count = max(counts.values())

    # If every word appears only once (has count=1), they all get a value of 5 (midscore)
    if max_count == 1:
        return {word: 5 for word in counts.keys()}
    # imporance score is extracted by dividing count for the specific word by the word with the most ocurrences'count and multiplying by 10 (gives x/10)
    importance_scores = {
        word: max(1, round((count / max_count) * 10))
        for word, count in counts.items()
    }
    return importance_scores


def emphasize_target_words(text, counts, boost=1.0):
    """
    Looks for emphasis phrases like and boosts the count of
    the word immediately after each one by `boost` (default is +1.0). (not implemented yet)
    """
    emphasis_phrases = ["we are looking for", "company is looking for", "we need", "company needs"]
    text_lower = text.lower()

    for phrase in emphasis_phrases:
        idx = text_lower.find(phrase)
        while idx != -1:
            after_phrase = text_lower[idx + len(phrase):].strip()
            match = re.match(r"(\w+)", after_phrase)
            if match:
                word = lemmatize_word(match.group(1))
                counts[word] = counts.get(word, 0) + boost

            # Look for the next occurrence
            idx = text_lower.find(phrase, idx + 1)

    return counts


def normalize_token(token: str) -> str:
    """
    Convert token to Normalization Form KC (NFKC) form and strip whitespace, so 'é\u00a0' -> 'e'.
    """
    token = unicodedata.normalize("NFKC", token)
    return token.strip()
