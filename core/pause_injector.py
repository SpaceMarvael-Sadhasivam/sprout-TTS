import re

def inject_pauses(text):

    # ✅ Remove Markdown / formatting symbols
    text = re.sub(r"[`*_#~]", "", text)

    # ✅ Remove any strange leftover symbol clusters
    text = re.sub(r"[^\w\s.,:;!?-]", "", text)

    # ✅ Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # ✅ Prevent punctuation explosions
    text = re.sub(r"\.{2,}", ".", text)

    # ✅ Natural pacing (safe for gTTS)
    text = text.replace(".", ". ... ")
    text = text.replace(",", ", ... ")

    return text.strip()