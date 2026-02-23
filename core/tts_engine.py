import time
from gtts import gTTS

def synthesize_speech(text, output_file, language_code, retries=3):

    for attempt in range(retries):
        try:
            tts = gTTS(text=text, lang=language_code, slow=False)
            tts.save(output_file)
            return

        except Exception as e:
            print(f"TTS retry {attempt+1}: {e}")
            time.sleep(2)

    raise RuntimeError("gTTS synthesis failed after retries")