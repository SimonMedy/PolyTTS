from django.http import HttpResponse
from django.views.decorators.http import require_GET
from gradio_client import Client
from django.conf import settings


SPEAKERS = ["emily", "paul", "sophie", "steven"]
EMOTIONS = [
    "angry", "disgusted", "fearful",
    "happy", "sad", "surprised", "neutral",
]


@require_GET
def say_view(request):
    sentence = request.GET.get("sentence", "")
    speaker = request.GET.get("speaker", "emily")
    emotion = request.GET.get("emotion", "neutral")

    if not sentence:
        return HttpResponse("sentence parameter is required", status=400)
    if speaker not in SPEAKERS:
        return HttpResponse(f"speaker must be one of {SPEAKERS}", status=400)
    if emotion not in EMOTIONS:
        return HttpResponse(f"emotion must be one of {EMOTIONS}", status=400)

    try:
        client = Client("neuphonic/neutts-2e", token=settings.HF_TOKEN or None)
        result = client.predict(
            sentence,
            speaker,
            emotion,
            1.0,
            50,
            api_name="/infer",
        )
        with open(result, "rb") as f:
            audio_data = f.read()
        return HttpResponse(audio_data, content_type="audio/wav")

    except Exception as e:
        return HttpResponse(str(e), status=500)
