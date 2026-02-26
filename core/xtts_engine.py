import os
import torch
from TTS.api import TTS

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading XTTS-v2 on {DEVICE}...")

tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2"
).to(DEVICE)


def synthesize_speech(text, output_file, speaker_wav):

    if not text or not text.strip():
        raise RuntimeError("Empty text passed to XTTS")

    if not isinstance(speaker_wav, str):
        raise RuntimeError(f"Invalid speaker_wav value: {speaker_wav}")

    if not os.path.exists(speaker_wav):
        raise RuntimeError(f"Speaker WAV file not found: {speaker_wav}")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    tts.tts_to_file(
        text=text,
        file_path=output_file,
        speaker_wav=speaker_wav,
        language="en"
    )

    return output_file