import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)


def optimize_for_tts(raw_text):

    prompt = f"""
Rewrite the following content as continuous spoken teaching by a human instructor.

You MUST fundamentally change how the text is expressed.

Strict enforcement rules:

- Completely eliminate ALL headings, labels, bullet points, list markers, and section names
- Do NOT preserve original sentence structure
- Do NOT keep original phrasing
- Reconstruct the explanation as natural lecture speech
- Present ideas as if verbally teaching students step-by-step
- Use conversational teaching language
- Expand compact statements into spoken reasoning
- Preserve ALL information exactly
- Do NOT summarize
- Do NOT shorten
- Output ONLY the lecture narration

Content:
{raw_text}
"""


    response = model.generate_content(prompt)

    return response.text.strip()