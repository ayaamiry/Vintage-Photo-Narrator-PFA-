# 📷 Vintage Photo Narrator

Une application web basée sur l'intelligence artificielle qui transforme
des photographies anciennes en histoires narratives personnalisées.

## Description

Vintage Photo Narrator combine un modèle de vision (VLM) et un modèle
de langage (LLM), tous deux fournis par l'API Google Gemini, pour analyser
une photographie ancienne et générer un récit immersif et cohérent.
La narration peut ensuite être écoutée grâce à la synthèse vocale ElevenLabs.

## Fonctionnalités

- Upload d'une photographie ancienne (JPG, PNG, WEBP)
- Analyse visuelle automatique via Gemini (VLM)
- Génération d'une histoire narrative via Gemini (LLM)
- Personnalisation : genre narratif, époque, détail clé
- Synthèse vocale avec choix de voix (homme/femme) via ElevenLabs
- Interface vintage élégante avec Streamlit + CSS personnalisé

## Installation

1. Cloner le projet :
   git clone https://github.com/votre-repo/vintage-photo-narrator.git
   cd vintage-photo-narrator

2. Installer les dépendances :
   pip install -r requirements.txt

3. Configurer les clés API dans app.py :
   GEMINI_API_KEY = "AIza..."

   Et dans tts.py :
   api_key="sk_..."

4. Lancer l'application :
   streamlit run app.py

## Structure du projet

vintage_photo_narrator/

├── app.py          # Interface Streamlit principale

├── vlm.py          # Modèle de vision (analyse de la photo)

├── llm.py          # Modèle de langage (génération de l'histoire)

├── tts.py          # Synthèse vocale (ElevenLabs)

├── prompts.py      # Prompts VLM et LLM

├── requirements.txt

└── README.md

## Technologies

- Python 3.14
- Streamlit
- Google Gemini API (gemini-2.0-flash-lite)
- ElevenLabs API (eleven_multilingual_v2)
- Pillow (PIL)

## Projet

Projet de Fin d'Année PFA-1A
ENSIAS — Université Mohammed V, Rabat
2025–2026
