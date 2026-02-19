from gtts import gTTS

def synthesize_speech(text, output_file, language_code):
    tts = gTTS(text=text, lang=language_code, slow=False)
    tts.save(output_file)
