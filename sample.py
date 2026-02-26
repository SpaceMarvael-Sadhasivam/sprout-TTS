from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

voices = client.voices.get_all()

for v in voices.voices:
    print(v.name, "→", v.voice_id)