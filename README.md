# NeuTTS-API

API Django REST pour du Text-to-Speech avec emotions, utilisant le modele [NeuTTS-2E](https://huggingface.co/neuphonic/neutts-2e) sur HuggingFace.

## Fonctionnement

```
Frontend → GET /say/ → Django → gradio_client → HuggingFace Space → WAV
```

## Setup

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

## Configuration

Creer un fichier `.env` a la racine :

```
HF_TOKEN=ton_token_hugging_face
```

Le token est requis pour l'acces au ZeroGPU. En creer un sur https://huggingface.co/settings/tokens

## Lancement

```bash
python manage.py runserver 127.0.0.1:8000
```

Ouvrir http://127.0.0.1:8000/

## API

```
GET /say/?sentence=Bonjour&speaker=emily&emotion=happy
```

| Parametre | Valeurs |
|-----------|---------|
| sentence | texte a convertir en audio |
| speaker | `emily`, `paul`, `sophie`, `steven` |
| emotion | `angry`, `disgusted`, `fearful`, `happy`, `sad`, `surprised`, `neutral` |

Reponse : fichier WAV (audio/wav)

## Stack

- Django 5.2 + Django REST Framework
- gradio_client
- NeuTTS-2E (HuggingFace Space)
