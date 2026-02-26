import requests
import os
from config import DEEPGRAM_API_KEY, DEEPGRAM_VOICE

DEEPGRAM_URL = "https://api.deepgram.com/v1/speak"

headers = {
    "Authorization": f"Token {DEEPGRAM_API_KEY}",
    "Content-Type": "application/json"
}


def synthesize_speech(text, output_file):

    if not text or not text.strip():
        raise RuntimeError("Empty text passed to TTS")

    payload = {
        "text": text
    }

    # Deepgram Aura models REQUIRE full model identifiers
    params = {
        "model": f"aura-2-{DEEPGRAM_VOICE}",
        "encoding": "mp3"
    }

    response = requests.post(
        DEEPGRAM_URL,
        headers=headers,
        json=payload,
        params=params
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Deepgram TTS Error | Status: {response.status_code} | "
            f"Response: {response.text}"
        )

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "wb") as f:
        f.write(response.content)

    return output_file