import re


def clean_word(text: str) -> str:
    """Extract and clean a single English word from selected text."""
    text = text.strip()
    # Remove surrounding punctuation/quotes
    text = re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', text)
    # If multiple words, take the first one
    words = text.split()
    if not words:
        return ''
    word = words[0].lower()
    # Only keep alphabetic characters and hyphens
    word = re.sub(r'[^a-z\-]', '', word)
    return word
