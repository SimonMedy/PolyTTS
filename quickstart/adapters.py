from django.conf import settings
from gradio_client import Client


NEUTTS_SPEAKERS = ["emily", "paul", "sophie", "steven"]
NEUTTS_EMOTIONS = [
    "angry", "disgusted", "fearful",
    "happy", "sad", "surprised", "neutral",
]

KOKORO_VOICES = {
    "af_alloy": "Alloy (US)",
    "af_aoede": "Aoede (US)",
    "af_jessica": "Jessica (US)",
    "af_kore": "Kore (US)",
    "af_nova": "Nova (US)",
    "af_river": "River (US)",
    "am_echo": "Echo (US)",
    "am_eric": "Eric (US)",
    "am_fenrir": "Fenrir (US)",
    "am_liam": "Liam (US)",
    "am_onyx": "Onyx (US)",
    "am_puck": "Puck (US)",
    "bf_alice": "Alice (UK)",
    "bf_lily": "Lily (UK)",
    "bm_daniel": "Daniel (UK)",
    "bm_fable": "Fable (UK)",
}

K2FSA_LANGUAGES = [
    "English", "French", "German", "Spanish", "Portuguese",
    "Italian", "Russian", "Chinese (Mandarin, \u666e\u901a\u8bdd)",
    "Japanese", "Korean", "Arabic", "Hindi",
    "Dutch", "Polish", "Swedish", "Turkish",
    "Czech", "Danish", "Finnish", "Greek",
    "Hungarian", "Indonesian", "Norwegian", "Romanian",
    "Ukrainian", "Vietnamese", "Bulgarian", "Catalan",
    "Croatian", "Estonian", "Lithuanian", "Slovak",
    "Slovenian", "Swahili", "Bengali", "Persian",
    "Thai", "Welsh", "Basque", "Kurdish", "Urdu",
]

KITTEN_MODELS = [
    "Nano (15M - Fastest)",
    "Micro (40M - Balanced)",
    "Mini (80M - Best Quality)",
]
KITTEN_VOICES = ["Bella", "Jasper", "Luna", "Bruno", "Rosie", "Hugo", "Kiki", "Leo"]


def _get_client(space_id):
    token = settings.HF_TOKEN or None
    return Client(space_id, token=token)


def generate_neutts(sentence, speaker, emotion):
    client = _get_client("neuphonic/neutts-2e")
    result = client.predict(sentence, speaker, emotion, 1.0, 50, api_name="/infer")
    with open(result, "rb") as f:
        return f.read()


def generate_kokoro(sentence, voice, speed):
    client = _get_client("Remsky/Kokoro-TTS-Zero")
    result = client.predict(
        sentence,
        [voice],
        speed,
        api_name="/generate_speech_from_ui",
    )
    audio_path = result[0] if isinstance(result, tuple) else result
    with open(audio_path, "rb") as f:
        return f.read()


def generate_k2fsa(sentence, language, speed):
    client = _get_client("k2-fsa/text-to-speech")
    models_resp = client.predict(language, api_name="/update_model_dropdown")
    model_value = models_resp["choices"][0][0]
    result = client.predict(
        language,
        model_value,
        sentence,
        "0",
        speed,
        api_name="/process",
    )
    audio_path = result[0]
    with open(audio_path, "rb") as f:
        return f.read()


def generate_kitten(sentence, model_name, voice, speed):
    client = _get_client("KittenML/KittenTTS-Demo")
    result = client.predict(sentence, model_name, voice, speed, api_name="/synthesize")
    with open(result, "rb") as f:
        return f.read()
