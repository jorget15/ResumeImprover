import json
import os
import re
import nltk
import nltk.data
import unicodedata
from nltk import WordNetLemmatizer, pos_tag
from nltk.corpus import wordnet


nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data")
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

# Updated list of resources to include
# - wordnet (for lemmatizer)
# - omw-1.4 (for WordNet synonyms)
# - punkt (for tokenization, if you use nltk.word_tokenize)
# - averaged_perceptron_tagger_eng (the modern English POS tagger model)
nltk_resources = [
    "wordnet",
    "omw-1.4",
    "punkt",
    "averaged_perceptron_tagger_eng"
]

def ensure_nltk_resources():
    """Ensure all required NLTK models are installed."""
    for resource in nltk_resources:
        try:
            # Each resource is stored in a slightly different subfolder:
            # - corpora/wordnet, corpora/omw-1.4
            # - tokenizers/punkt
            # - taggers/averaged_perceptron_tagger_eng
            # But calling nltk.download(...) with the short name
            # automatically puts it in the correct subfolder.
            nltk.data.find(resource)  # Will raise LookupError if not installed
        except LookupError:
            nltk.download(resource, download_dir=nltk_data_path)

# Initialize NLTK resources at import
ensure_nltk_resources()

print("✅ NLTK is now using this path:", nltk.data.path)


def load_excluded_words(company_name=None):
    """
    Loads excluded words from excluded_words.json. Optionally excludes the company name.
    JSON can have categories or plain lists, but we flatten them into one set.
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

    # Exclude company name if provided
    if company_name and company_name.strip():
        excluded_words.add(company_name.lower().strip())

    return excluded_words

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    """Map POS tag to first character WordNetLemmatizer understands."""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)  # Default to NOUN

def lemmatize_word(word):
    """
    Lemmatizes a single token. Also handles some manual special cases:
    e.g., 'engineering' -> 'engineer', 'programming' -> 'program'.
    """
    lemma = lemmatizer.lemmatize(word.lower(), get_wordnet_pos(word))
    special_cases = {
        "engineering": "engineer",
        "programming": "program",
        "developing": "develop",
        "analyzing": "analyze",
    }
    return special_cases.get(lemma, lemma)

def calculate_importance(counts):
    """
    Assigns importance scores from 1 to 10. The highest-count word gets 10,
    scaling down proportionally for others.
    """
    if not counts:
        return {}

    max_count = max(counts.values())

    # If everything has count=1, let's give them all midscore=5
    if max_count == 1:
        return {word: 5 for word in counts.keys()}

    importance_scores = {
        word: max(1, round((count / max_count) * 10))
        for word, count in counts.items()
    }
    return importance_scores

def emphasize_target_words(text):
    """
    Example function that identifies words after phrases like 'we are looking for'.
    Not widely used in your code, but kept if you want to highlight target words.
    """
    emphasis_phrases = ["we are looking for", "company is looking for", "we need", "company needs"]
    results = []
    text_lower = text.lower()
    for phrase in emphasis_phrases:
        idx = text_lower.find(phrase)
        if idx != -1:
            after_phrase = text_lower[idx + len(phrase):].strip()
            match = re.match(r"(\w+)", after_phrase)
            if match:
                results.append(lemmatize_word(match.group(1)))
    return results

def normalize_token(token: str) -> str:
    """
    Convert token to NFKC form and strip whitespace, so 'a\u00a0' -> 'a'.
    Defined here in case you want to share across code.
    """
    token = unicodedata.normalize("NFKC", token)
    return token.strip()
