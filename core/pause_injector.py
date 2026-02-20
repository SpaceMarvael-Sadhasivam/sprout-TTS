import re

def inject_pauses(text):
    """
    Convert punctuation into gTTS-friendly pauses.
    """

    # Normalize whitespace first
    text = re.sub(r"\s+", " ", text)

    # Strong pause (sentence end)
    text = text.replace(".", "... ")

    # Short pause
    text = text.replace(",", ", ... ")

    # Medium pause
    text = text.replace(":", ": ... ")

    # Slight rhetorical pause
    text = text.replace(";", "; ... ")

    return text.strip()
