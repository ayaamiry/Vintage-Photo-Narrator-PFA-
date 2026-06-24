from elevenlabs.client import ElevenLabs
import tempfile

VOICES = {
    "Femme — Bella": "EXAVITQu4vr4xnSDxMaL",
    "Homme — Adam":  "pNInz6obpgDQGcFmaJgB",
}

def text_to_speech(text: str, voice_choice: str = "Homme — Adam") -> str:
    client = ElevenLabs(api_key="sk_18f6987664db7488851faf9528e1fd02f9b5a57a9b9ea979")
    voice_id = VOICES.get(voice_choice, "pNInz6obpgDQGcFmaJgB")
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2",
    )
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.close()
    with open(tmp.name, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    return tmp.name