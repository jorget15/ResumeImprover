import json
import re
from nltk import WordNetLemmatizer, pos_tag
from nltk.corpus import wordnet
import nltk
import os

# List of required NLTK resources
nltk_resources = [
    "averaged_perceptron_tagger",
    "wordnet",
    "omw-1.4"
]


# Function to check and download missing NLTK resources
def ensure_nltk_resources():
    for resource in nltk_resources:
        try:
            nltk.data.find(f"taggers/{resource}")  # Check if resource exists
        except LookupError:
            nltk.download(resource)  # Download only if missing


# Ensure resources are available at runtime
ensure_nltk_resources()


def load_excluded_words():
    """Loads excluded words (common verbs, prepositions, etc.) from the correct file location."""
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
    filepath = os.path.join(script_dir, "excluded_words.json")  # Ensure absolute path

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Error: Excluded words file not found at {filepath}")

    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    return set(data["excluded_words"])


lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(word):
    """Map POS tag to first character WordNetLemmatizer understands."""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)  # Default to NOUN if not found


def lemmatize_word(word):
    """Lemmatizes a word based on its part of speech and handles special cases manually."""
    lemma = lemmatizer.lemmatize(word.lower(), get_wordnet_pos(word))

    # Manually handling common edge cases (e.g., engineering -> engineer)
    special_cases = {
        "engineering": "engineer",
        "programming": "program",
        "developing": "develop",
        "analyzing": "analyze",
    }

    return special_cases.get(lemma, lemma)


def calculate_importance(counts):
    """Assigns importance scores from 1 to 10, ensuring consistency across keywords and bigrams."""
    if not counts:
        return {}

    max_count = max(counts.values())

    # Avoid division errors and ensure proper scaling
    if max_count == 1:
        return {word: 5 for word in counts.keys()}  # Assign middle score if everything appears only once

    importance_scores = {
        word: max(1, round((count / max_count) * 10))  # Ensure scaling works consistently
        for word, count in counts.items()
    }

    return importance_scores


def emphasize_target_words(text):
    """Identifies and emphasizes words that come after key hiring phrases."""
    emphasis_phrases = [
        "we are looking for", "company is looking for", "we need", "company needs"
    ]
    words_to_emphasize = []

    text_lower = text.lower()
    for phrase in emphasis_phrases:
        start = text_lower.find(phrase)
        if start != -1:
            after_phrase = text_lower[start + len(phrase):].strip()
            match = re.match(r"(\w+)", after_phrase)
            if match:
                words_to_emphasize.append(lemmatize_word(match.group(1)))

    return words_to_emphasize
