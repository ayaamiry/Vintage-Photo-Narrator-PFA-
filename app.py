import streamlit as st
from PIL import Image
import io
from vlm import analyze_image
from llm import generate_story
from tts import text_to_speech
import os

GEMINI_API_KEY = "AQ.Ab8RN6JyGgRUXSkQQRW2fgJW8eeL9tZl_GaRKcV0_ud6hzcJ2A"

st.set_page_config(
    page_title="Vintage Photo Narrator",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400;1,500&family=Crimson+Pro:ital,wght@0,300;0,400;1,300;1,400&display=swap');

html, body  {
    background-color: #FFF9F3 !important;
    color: #443223 !important;
    font-family: 'Crimson Pro', Georgia, serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    max-width: 880px !important;
    padding: 2rem 2.5rem 5rem !important;
}

.app-header {
    text-align: center;
    padding: 3rem 0 2.5rem;
    border-bottom: 1px solid #DBC4A5;
    margin-bottom: 3rem;
}
.eyebrow {
    font-family: 'Crimson Pro', serif;
    font-size: 10px;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: #A08670;
    margin-bottom: 1rem;
}
.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 400;
    font-style: italic;
    color: #443223;
    line-height: 1.1;
    margin: 0 0 0.8rem;
}
.main-subtitle {
    font-size: 1.05rem;
    font-style: italic;
    font-weight: 300;
    color: #A08670;
    line-height: 1.7;
}

.section-label {
    font-family: 'Crimson Pro', serif;
    font-size: 10px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #A08670;
    margin: 2rem 0 0.6rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #DBC4A5;
}

[data-testid="stFileUploader"] {
    border: 2px dashed #DBC4A5 !important;
    border-radius: 16px !important;
    background: #FFFCF8 !important;
    padding: 2rem 1.5rem !important;
    transition: all 0.25s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: #A08670 !important;
    background: #FFF9F3 !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] > div > span {
    font-family: 'Playfair Display', serif !important;
    font-style: italic !important;
    font-size: 1.1rem !important;
    color: #A08670 !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] > div > small {
    font-family: 'Crimson Pro', serif !important;
    color: #DBC4A5 !important;
    font-style: italic !important;
}
[data-testid="stFileUploader"] button {
    font-family: 'Crimson Pro', serif !important;
    background: transparent !important;
    border: 1px solid #DBC4A5 !important;
    color: #72583E !important;
    border-radius: 6px !important;
    font-style: italic !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: #FFF9F3 !important;
    border: 1px solid #DBC4A5 !important;
    border-radius: 8px !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 1rem !important;
    font-style: italic !important;
}

/* Text input */
[data-testid="stTextInput"] > div > div > input {
    background: #FFF9F3 !important;
    border: 1px solid #DBC4A5 !important;
    border-radius: 8px !important;
    color: #443223 !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 1rem !important;
    font-style: italic !important;
    padding: 0.5rem 0.75rem !important;
} 

[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #A08670 !important;
    box-shadow: none !important;
}
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] li {
    font-family: 'Crimson Pro', serif !important;
    font-style: italic !important;
    color: #443223 !important;
}

label[data-testid="stWidgetLabel"] p {
    font-family: 'Crimson Pro', serif !important;
    font-size: 0.85rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #A08670 !important;
}

.stButton > button {
    width: 100% !important;
    background-color: #443223 !important;
    color: #FFF9F3 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 1rem 2rem !important;
    font-family: 'Playfair Display', serif !important;
    font-style: italic !important;
    font-size: 1.2rem !important;
    font-weight: 400 !important;
    letter-spacing: 1px !important;
    transition: all 0.2s ease !important;
    margin-top: 1.2rem !important;
}
.stButton > button:hover {
    background-color: #72583E !important;
    color: #FFF9F3 !important;
}
.stButton > button:disabled {
    background-color: #DBC4A5 !important;
    color: #A08670 !important;
    cursor: not-allowed !important;
}

[data-testid="stImage"] img {
    border-radius: 12px !important;
    border: 1px solid #DBC4A5 !important;
    filter: sepia(20%) contrast(1.04) saturate(0.88);
    width: 100% !important;
}

hr {
    border: none !important;
    border-top: 1px solid #DBC4A5 !important;
    margin: 2.5rem 0 !important;
}

.story-card {
    background: #FFF9F3;
    border: 1px solid #DBC4A5;
    border-radius: 16px;
    padding: 2rem 2rem 1.8rem;
    margin-bottom: 1rem;
}
.story-badge {
    display: inline-block;
    background: #DBC4A5;
    color: #72583E;
    font-family: 'Crimson Pro', serif;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 1.2rem;
}
.story-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    font-style: italic;
    font-weight: 400;
    color: #443223;
    margin: 0 0 1.4rem;
    line-height: 1.3;
}
.story-body {
    font-family: 'Crimson Pro', serif;
    font-size: 1.05rem;
    font-weight: 300;
    line-height: 2;
    color: #443223;
}
.story-placeholder {
    font-family: 'Crimson Pro', serif;
    font-style: italic;
    color: #DBC4A5;
    font-size: 1rem;
    line-height: 1.8;
    text-align: center;
    padding: 1.5rem 0;
}


[data-testid="stAlert"] {
    font-family: 'Crimson Pro', serif !important;
    font-style: italic !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
}

[data-testid="stSidebar"] {
    background-color: #F5EDE0 !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem !important;
}

.app-footer {
    text-align: center;
    margin-top: 5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #DBC4A5;
    font-family: 'Crimson Pro', serif;
    font-style: italic;
    color: #A08670;
    font-size: 0.88rem;
    line-height: 1.9;
}
.app-footer span {
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #DBC4A5;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="font-family: 'Playfair Display', serif; font-style: italic;
                font-size: 1.3rem; color: #443223; margin-bottom: 0.4rem;">
        Configuration
    </div>
    <div style="font-family: 'Crimson Pro', serif; font-size: 0.85rem;
                font-style: italic; color: #A08670; line-height: 1.7; margin-bottom: 1.2rem;">
        Clé API intégrée · Gemini 2.5 Flash
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family: 'Crimson Pro', serif; font-size: 0.82rem;
                font-style: italic; color: #A08670; line-height: 1.75;">
        Modèle utilisé :<br>
        <strong style="color: #72583E;">gemini-2.5-flash</strong><br><br>
        Projet de Fin d'Année · PFA-1A<br>
        Vision &amp; Language Models
    </div>
    """, unsafe_allow_html=True)

#  HEADER
st.markdown("""
<div class="app-header">
    <div class="eyebrow">✦ &nbsp; Narrateur de Photographies Anciennes &nbsp; ✦</div>
    <div class="main-title">Vintage Photo Narrator</div>
    <div class="main-subtitle">
        Chaque photographie ancienne cache une histoire oubliée.<br>
        Laissez l'intelligence artificielle la retrouver pour vous.
    </div>
</div>
""", unsafe_allow_html=True)

#  UPLOAD
st.markdown('<div class="section-label">① &nbsp; Votre photographie</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    label="Upload",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed",
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True, caption="Votre photographie · prête à être narrée")

#  OPTIONS
st.markdown('<div class="section-label">② &nbsp; Options narratives &nbsp;(facultatif)</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    mood = st.selectbox(
        "Genre / Ambiance",
        options=[
            "— Laisser la photo décider —",
            "Mystérieux",
            "Romantique",
            "Mélancolique",
            "Chaleureux",
            "Aventurier",
            "Historique",
            "Amer-doux",
        ],
    )


with col2:
    period = st.text_input(
        "Époque",
        placeholder="Ex : années 1940, ère victorienne…",
    )

detail = st.text_input(
    "Détail clé à inclure",
    placeholder="Ex : le chapeau de la femme, la vieille voiture, le chien en arrière-plan…",
)

# ─── BOUTON ───
st.markdown('<div class="section-label">③ &nbsp; Génération</div>', unsafe_allow_html=True)

generate = st.button(
    "✦  Révéler l'Histoire  ✦",
    disabled=(uploaded_file is None),
    use_container_width=True,
)

# ─── GÉNÉRATION ───
if generate and uploaded_file:
    image_bytes = uploaded_file.getvalue()
    genre_val  = None if mood == "— Laisser la photo décider —" else mood
    era_val    = period.strip() or None
    detail_val = detail.strip() or None

    with st.spinner("Analyse de la photographie en cours…"):
        try:
            description = analyze_image(image_bytes, GEMINI_API_KEY)
        except Exception as e:
            st.error(f"Vision model error : {e}")
            st.stop()

    with st.spinner("L'histoire prend forme…"):
        try:
            story_raw = generate_story(
                description, GEMINI_API_KEY,
                genre=genre_val, era=era_val, detail=detail_val,
            )
        except Exception as e:
            st.error(f"Language model error : {e}")
            st.stop()

    lines = story_raw.strip().splitlines()
    title_line, body_lines = "", []
    for line in lines:
        stripped = line.strip().lstrip("#").strip().strip("*").strip()
        if stripped and not title_line:
            title_line = stripped
        elif stripped:
            body_lines.append(line)

    # ── Sauvegarder dans session_state ──
    st.session_state["story_body"]   = "\n".join(body_lines).strip()
    st.session_state["title_line"]   = title_line
    st.session_state["description"]  = description
    st.session_state["image_bytes"]  = image_bytes
    st.session_state["genre_val"]    = genre_val
    st.session_state["era_val"]      = era_val

# ─── AFFICHAGE (persiste même après clic audio) ───
if "story_body" in st.session_state:
    st.markdown("<hr>", unsafe_allow_html=True)

    left, right = st.columns([1, 1.6], gap="large")

    with left:
        st.image(
            Image.open(io.BytesIO(st.session_state["image_bytes"])),
            use_container_width=True,
            caption="La photographie qui a inspiré l'histoire",
        )

    with right:
        badge        = st.session_state["genre_val"] or "Photographie Ancienne"
        period_badge = f" · {st.session_state['era_val']}" if st.session_state["era_val"] else ""

        st.markdown(f"""
        <div class="story-card">
            <div class="story-badge">{badge}{period_badge}</div>
            <div class="story-title">{st.session_state['title_line']}</div>
            <div class="story-body">{st.session_state['story_body'].replace(chr(10), '<br>')}</div>
        </div>
        """, unsafe_allow_html=True)

    # ─── TTS ─── (à l'intérieur du if, même niveau que left/right)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">🔊 &nbsp; Écouter l\'histoire</div>', unsafe_allow_html=True)

    voice_choice = st.selectbox(
        "Voix du narrateur",
        options=["Femme — Bella", "Homme — Adam"],
    )

    if st.button("▶  Générer la narration audio", use_container_width=True):
        with st.spinner("Synthèse vocale en cours…"):
            try:
                audio_path = text_to_speech(st.session_state["story_body"], voice_choice)
                with open(audio_path, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
                os.unlink(audio_path)
            except Exception as e:
                st.warning(f"TTS non disponible : {e}")

# ─── FOOTER ─── (en dehors du if)
st.markdown("""
<div class="app-footer">
    Vintage Photo Narrator · Projet de Fin d'Année PFA-1A<br>
""", unsafe_allow_html=True)