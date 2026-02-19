import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)


def optimize_for_tts(raw_text):

    prompt = f"""
Rewrite the following text so it sounds natural when read aloud by a human narrator.

Narration rules:

- Preserve the original meaning exactly
- Improve sentence flow and punctuation for speech
- Remove visual-only artifacts (page numbers, headers, footers)
- Ignore or eliminate special characters that would sound unnatural when spoken
- Do not read symbols literally unless they are semantically important
- Expand abbreviations only when necessary for clarity
- Format the text the way a person would naturally read a book or document aloud
- Do NOT add new information
- Output only the rewritten narration text

Text:
{raw_text}
"""


    response = model.generate_content(prompt)

    return response.text.strip()
