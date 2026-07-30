# PolyTTS

![Frontend](assets/image.png)

API Django REST pour du Text-to-Speech multi-modeles, avec frontend Tailwind CSS et dark mode.

## Modeles

| Modele | Langues | Voix | Infra |
|--------|---------|------|-------|
| **K2-FSA** | 40+ langues | — | CPU, sans limite |
| **Kokoro-TTS** | EN (US+UK) | 28 voix | CPU, sans limite |
| **NeuTTS-2E** | EN | 4 speakers, 7 emotions | ZeroGPU |
| **KittenTTS** | EN | 8 voix, 3 tailles | CPU |

## Fonctionnement

```
Frontend → GET /say/ → Django → gradio_client → HuggingFace Space → WAV
```

## Setup

```bash
python -m venv .venv
\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

## Configuration

Creer un fichier `.env` a la racine :

```
HF_TOKEN=ton_token_hugging_face
```

Le token est requis pour l'acces aux HuggingFace Spaces. En creer un sur https://huggingface.co/settings/tokens

## Lancement

```bash
python manage.py runserver 127.0.0.1:8000
```

Ouvrir http://127.0.0.1:8000/

## API

```
GET /say/?sentence=Bonjour&model=k2fsa&language=French
```

| Parametre | Description |
|-----------|-------------|
| sentence | Texte a convertir en audio |
| model | `k2fsa`, `kokoro`, `neutts`, `kitten` |
| language | K2-FSA : langue du texte |
| voice | Kokoro : voix (`af_heart`, `bf_emma`...) / NeuTTS : speaker / Kitten : voix |
| speed | Vitesse (0.5 - 2.0) |
| emotion | NeuTTS uniquement (`happy`, `sad`...) |
| model_size | KittenTTS : `Nano (15M)`, `Micro (40M)`, `Mini (80M)` |

Reponse : fichier WAV (audio/wav)


## Stack

- Django 5.2 + Django REST Framework
- gradio_client
- HuggingFace Spaces (K2-FSA, Kokoro, NeuTTS, KittenTTS)
