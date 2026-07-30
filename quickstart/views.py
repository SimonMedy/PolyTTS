from django.http import HttpResponse
from django.views.decorators.http import require_GET
from quickstart.adapters import (
    generate_neutts,
    generate_kokoro,
    generate_kitten,
    generate_inflect,
    NEUTTS_SPEAKERS,
    NEUTTS_EMOTIONS,
    KOKORO_VOICES,
    KITTEN_MODELS,
    KITTEN_VOICES,
    INFLECT_MODELS,
)


@require_GET
def say_view(request):
    model = request.GET.get("model", "kokoro")
    sentence = request.GET.get("sentence", "")

    if not sentence:
        return HttpResponse("sentence parameter is required", status=400)

    try:
        if model == "kokoro":
            voice = request.GET.get("voice", "af_alloy")
            speed = float(request.GET.get("speed", "1.0"))
            if voice not in KOKORO_VOICES:
                return HttpResponse(f"voice must be one of {list(KOKORO_VOICES.keys())}", status=400)
            if not 0.5 <= speed <= 2.0:
                return HttpResponse("speed must be between 0.5 and 2.0", status=400)
            audio_data = generate_kokoro(sentence, voice, speed)

        elif model == "neutts":
            speaker = request.GET.get("speaker", "emily")
            emotion = request.GET.get("emotion", "neutral")
            if speaker not in NEUTTS_SPEAKERS:
                return HttpResponse(f"speaker must be one of {NEUTTS_SPEAKERS}", status=400)
            if emotion not in NEUTTS_EMOTIONS:
                return HttpResponse(f"emotion must be one of {NEUTTS_EMOTIONS}", status=400)
            audio_data = generate_neutts(sentence, speaker, emotion)

        elif model == "kitten":
            model_name = request.GET.get("model_name", "Micro (40M - Balanced)")
            voice = request.GET.get("voice", "Jasper")
            speed = float(request.GET.get("speed", "1.0"))
            if model_name not in KITTEN_MODELS:
                return HttpResponse(f"model_name must be one of {KITTEN_MODELS}", status=400)
            if voice not in KITTEN_VOICES:
                return HttpResponse(f"voice must be one of {KITTEN_VOICES}", status=400)
            if not 0.5 <= speed <= 2.0:
                return HttpResponse("speed must be between 0.5 and 2.0", status=400)
            audio_data = generate_kitten(sentence, model_name, voice, speed)

        elif model == "inflect":
            model_name = request.GET.get("model_name", "Inflect Nano v2 (4M)")
            speed = float(request.GET.get("speed", "1.0"))
            variation = float(request.GET.get("variation", "0.667"))
            pitch = float(request.GET.get("pitch", "0.0"))
            if model_name not in INFLECT_MODELS:
                return HttpResponse(f"model_name must be one of {INFLECT_MODELS}", status=400)
            if not 0.5 <= speed <= 2.0:
                return HttpResponse("speed must be between 0.5 and 2.0", status=400)
            audio_data = generate_inflect(sentence, model_name, speed, variation, pitch)

        else:
            return HttpResponse("model must be 'kokoro', 'neutts', 'kitten' or 'inflect'", status=400)

        return HttpResponse(audio_data, content_type="audio/wav")

    except Exception as e:
        return HttpResponse(str(e), status=500)
