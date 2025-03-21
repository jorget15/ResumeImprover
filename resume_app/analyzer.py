import json
import re
from nltk import WordNetLemmatizer, pos_tag
from nltk.corpus import wordnet
import nltk
import os
import nltk.data

# Force NLTK to use the correct path on both local and Streamlit Cloud
nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data")
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

nltk.data.path.append(nltk_data_path)  # Ensure correct path

# List of required NLTK resources
nltk_resources = [
    "averaged_perceptron_tagger",
    "wordnet",
    "omw-1.4"
    "taggers/averaged_perceptron_tagger_eng"  # Explicitly include this missing one
]


# Function to check and download missing NLTK resources
def ensure_nltk_resources():
    for resource in nltk_resources:
        try:
            nltk.data.find(resource)  # Check if resource exists
        except LookupError:
            nltk.download(resource.split('/')[-1], download_dir=nltk_data_path)  # Download only if missing


# Ensure resources are available at runtime
ensure_nltk_resources()

print("✅ NLTK is now using this path:", nltk.data.path)  # Debug print


def load_excluded_words(company_name=None):
    """Loads excluded words across all categories while keeping company tools and technologies."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excluded_filepath = os.path.join(script_dir, "excluded_words.json")

    excluded_words = set()

    if os.path.exists(excluded_filepath):
        with open(excluded_filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Flatten any nested lists in JSON to ensure all words are added
            for category_list in data.values():
                if isinstance(category_list, list):  # Make sure it's actually a list
                    for word in category_list:
                        if isinstance(word, list):  # If there's another nested list, unpack it
                            excluded_words.update(w.lower() for w in word)
                        else:
                            excluded_words.add(word.lower())

    # Add company name (if provided) to the excluded words list
    if company_name and company_name.strip():
        excluded_words.add(company_name.lower().strip())

    return excluded_words


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
