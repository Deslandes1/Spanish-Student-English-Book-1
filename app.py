import streamlit as st
import base64
from io import BytesIO
from gtts import gTTS
import json

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Let's Learn English With Gesner",
    page_icon="🇺🇸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- TITLE & CONTACT ----------
st.markdown("""
# 🇺🇸 Let's Learn English With Gesner
### 📖 Aprendamos Inglés con Gesner – Libro 1
""")
st.markdown("""
**👨‍🏫 Teacher Gesner Deslandes**  
📞 (509)-4738-5663  
✉️ deslandes78@gmail.com
""")
st.markdown("---")

# ---------- CACHED AUDIO GENERATION ----------
@st.cache_data(show_spinner=False)
def get_audio_base64(text: str, lang: str = "en") -> str:
    """Generate audio for text and return base64 string for embedding."""
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    b64 = base64.b64encode(audio_bytes.read()).decode()
    return b64

def audio_player(text: str, lang: str = "en", key: str = None):
    """Display an audio play button with the given text."""
    if not text:
        return
    b64 = get_audio_base64(text, lang)
    audio_html = f"""
        <audio controls style="width: 100%; height: 30px;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            Your browser does not support audio.
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# ---------- BOOK DATA (inline JSON) ----------
# For production, you can load this from a separate JSON file.
BOOK_DATA = {
    "chapters": [
        {
            "number": 1,
            "title": "Introductions",
            "spanish_title": "Presentaciones",
            "conversations": [
                {
                    "english": "Hello, how are you?",
                    "spanish": "Hola, ¿cómo estás?"
                },
                {
                    "english": "I'm fine, thank you. And you?",
                    "spanish": "Estoy bien, gracias. ¿Y tú?"
                },
                {
                    "english": "My name is Maria. What's your name?",
                    "spanish": "Me llamo María. ¿Cómo te llamas?"
                }
            ],
            "vocabulary": [
                {"english": "hello", "spanish": "hola"},
                {"english": "goodbye", "spanish": "adiós"},
                {"english": "please", "spanish": "por favor"},
                {"english": "thank you", "spanish": "gracias"},
                {"english": "yes", "spanish": "sí"},
                {"english": "no", "spanish": "no"},
                {"english": "friend", "spanish": "amigo"},
                {"english": "teacher", "spanish": "profesor"},
                {"english": "student", "spanish": "estudiante"},
                {"english": "school", "spanish": "escuela"}
            ],
            "idioms": [
                {
                    "english": "Break a leg",
                    "english_explanation": "Good luck!",
                    "spanish": "Buena suerte",
                    "spanish_explanation": "¡Buena suerte!"
                },
                {
                    "english": "It's raining cats and dogs",
                    "english_explanation": "It's raining heavily.",
                    "spanish": "Está lloviendo a cántaros",
                    "spanish_explanation": "Llueve muy fuerte."
                },
                {
                    "english": "Piece of cake",
                    "english_explanation": "Very easy.",
                    "spanish": "Pan comido",
                    "spanish_explanation": "Muy fácil."
                },
                {
                    "english": "Hit the nail on the head",
                    "english_explanation": "To be exactly right.",
                    "spanish": "Dar en el clavo",
                    "spanish_explanation": "Estar exactamente en lo correcto."
                },
                {
                    "english": "Under the weather",
                    "english_explanation": "Feeling ill.",
                    "spanish": "Sentirse mal",
                    "spanish_explanation": "Sentirse enfermo."
                }
            ],
            "pronunciation": {
                "english_sentences": [
                    "She sells sea shells by the sea shore.",
                    "Peter Piper picked a peck of pickled peppers.",
                    "How can a clam cram in a clean cream can?",
                    "I scream, you scream, we all scream for ice cream.",
                    "Fuzzy Wuzzy was a bear.",
                    "Can you can a can as a canner can can a can?",
                    "Six thick thistle sticks.",
                    "The thirty-three thieves thought that they thrilled the throne.",
                    "Which witch is which?",
                    "Red leather, yellow leather."
                ],
                "spanish_sentences": [
                    "Ella vende conchas marinas en la orilla del mar.",
                    "Pedro Pérez picó un pico de pimientos encurtidos.",
                    "¿Cómo puede una almeja meterse en una lata de crema limpia?",
                    "Grito, tú gritas, todos gritamos por helado.",
                    "Fuzzy Wuzzy era un oso.",
                    "¿Puedes enlatar una lata como un enlatador puede enlatar una lata?",
                    "Seis palos de cardo gruesos.",
                    "Los treinta y tres ladrones pensaron que encantaron el trono.",
                    "¿Qué bruja es cuál?",
                    "Cuero rojo, cuero amarillo."
                ]
            },
            "grammar": {
                "rules": [
                    {
                        "english": "Use 'am' with the pronoun 'I' (e.g., I am a student).",
                        "spanish": "Usa 'am' con el pronombre 'I' (ej. I am a student)."
                    },
                    {
                        "english": "Use 'is' with he, she, it (e.g., She is a teacher).",
                        "spanish": "Usa 'is' con he, she, it (ej. She is a teacher)."
                    },
                    {
                        "english": "Use 'are' with you, we, they (e.g., We are friends).",
                        "spanish": "Usa 'are' con you, we, they (ej. We are friends)."
                    },
                    {
                        "english": "Add 's' to verbs for he/she/it in present simple (e.g., He speaks English).",
                        "spanish": "Añade 's' a los verbos para he/she/it en presente simple (ej. He speaks English)."
                    },
                    {
                        "english": "Use 'do/does' to form questions and negatives in present simple.",
                        "spanish": "Usa 'do/does' para formar preguntas y negativas en presente simple."
                    }
                ]
            },
            "exercises": {
                "class": {
                    "description": "Class Assignment – Complete these sentences with the correct verb form.",
                    "questions": [
                        {"question": "I ___ a student.", "answer": "am"},
                        {"question": "She ___ a teacher.", "answer": "is"},
                        {"question": "We ___ friends.", "answer": "are"},
                        {"question": "He ___ English.", "answer": "speaks"},
                        {"question": "___ you like coffee?", "answer": "Do"},
                        {"question": "They ___ not here.", "answer": "are"},
                        {"question": "It ___ a cat.", "answer": "is"},
                        {"question": "You ___ my best friend.", "answer": "are"},
                        {"question": "Maria and I ___ students.", "answer": "are"},
                        {"question": "The book ___ on the table.", "answer": "is"}
                    ]
                },
                "homework": {
                    "description": "Homework – Write the correct form of the verb in parentheses.",
                    "questions": [
                        {"question": "He (to be) a doctor.", "answer": "is"},
                        {"question": "We (to like) pizza.", "answer": "like"},
                        {"question": "She (to study) every day.", "answer": "studies"},
                        {"question": "I (to have) a car.", "answer": "have"},
                        {"question": "They (to go) to school.", "answer": "go"},
                        {"question": "You (to be) happy.", "answer": "are"},
                        {"question": "The dog (to eat) meat.", "answer": "eats"},
                        {"question": "My parents (to live) in Haiti.", "answer": "live"},
                        {"question": "It (to rain) a lot.", "answer": "rains"},
                        {"question": "We (to speak) Spanish and English.", "answer": "speak"}
                    ]
                }
            }
        }
        # Add more chapters here...
    ]
}

# ---------- SIDEBAR: CHAPTER SELECTION ----------
chapters = BOOK_DATA["chapters"]
chapter_options = [f"Chapter {ch['number']}: {ch['title']}" for ch in chapters]
selected_label = st.sidebar.selectbox("📚 Select Chapter", chapter_options)
selected_idx = chapter_options.index(selected_label)
chapter = chapters[selected_idx]

# ---------- DISPLAY CHAPTER CONTENT ----------
st.header(f"📘 Chapter {chapter['number']}: {chapter['title']}")
st.subheader(f"🇪🇸 {chapter['spanish_title']}")

# ---------- 1. CONVERSATIONS ----------
with st.expander("💬 1. Conversations / Conversaciones", expanded=True):
    for i, conv in enumerate(chapter["conversations"]):
        st.markdown(f"**Conversation {i+1}**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("🇺🇸 **English**")
            st.write(conv["english"])
            audio_player(conv["english"], "en", key=f"conv_en_{i}")
        with col2:
            st.markdown("🇪🇸 **Spanish**")
            st.write(conv["spanish"])
            audio_player(conv["spanish"], "es", key=f"conv_es_{i}")
        st.markdown("---")

# ---------- 2. VOCABULARY ----------
with st.expander("📝 2. Vocabulary / Vocabulario", expanded=True):
    for item in chapter["vocabulary"]:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{item['english']}**")
            audio_player(item["english"], "en", key=f"voc_en_{item['english']}")
        with col2:
            st.markdown(f"**{item['spanish']}**")
            audio_player(item["spanish"], "es", key=f"voc_es_{item['spanish']}")
        st.markdown("---")

# ---------- 3. IDIOMS ----------
with st.expander("🃏 3. Idioms / Modismos", expanded=True):
    for i, idiom in enumerate(chapter["idioms"]):
        st.markdown(f"**Idiom {i+1}**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("🇺🇸 **English**")
            st.markdown(f"*{idiom['english']}*")
            st.write(idiom["english_explanation"])
            audio_player(f"{idiom['english']}. {idiom['english_explanation']}", "en", key=f"idiom_en_{i}")
        with col2:
            st.markdown("🇪🇸 **Spanish**")
            st.markdown(f"*{idiom['spanish']}*")
            st.write(idiom["spanish_explanation"])
            audio_player(f"{idiom['spanish']}. {idiom['spanish_explanation']}", "es", key=f"idiom_es_{i}")
        st.markdown("---")

# ---------- 4. PRONUNCIATION ----------
with st.expander("🗣️ 4. Pronunciation / Pronunciación", expanded=True):
    st.markdown("**English Sentences / Frases en Inglés**")
    for i, sent in enumerate(chapter["pronunciation"]["english_sentences"]):
        st.write(sent)
        audio_player(sent, "en", key=f"pron_en_{i}")
    st.markdown("---")
    st.markdown("**Spanish Sentences / Frases en Español**")
    for i, sent in enumerate(chapter["pronunciation"]["spanish_sentences"]):
        st.write(sent)
        audio_player(sent, "es", key=f"pron_es_{i}")

# ---------- 5. GRAMMAR ----------
with st.expander("📖 5. Grammar / Gramática", expanded=True):
    for i, rule in enumerate(chapter["grammar"]["rules"]):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("🇺🇸 **English**")
            st.write(rule["english"])
            audio_player(rule["english"], "en", key=f"gram_en_{i}")
        with col2:
            st.markdown("🇪🇸 **Spanish**")
            st.write(rule["spanish"])
            audio_player(rule["spanish"], "es", key=f"gram_es_{i}")
        st.markdown("---")

# ---------- 6. EXERCISES ----------
with st.expander("✏️ 6. Exercises / Ejercicios", expanded=True):
    # Class Assignment
    st.subheader("📝 Class Assignment / Tarea en Clase")
    class_data = chapter["exercises"]["class"]
    st.write(class_data["description"])
    audio_player(class_data["description"], "en", key="class_desc_en")
    audio_player(class_data["description"], "es", key="class_desc_es")
    st.markdown("---")
    for i, q in enumerate(class_data["questions"]):
        st.markdown(f"{i+1}. {q['question']}")
        # Optionally, show answer with a button (hidden by default)
        if st.button(f"Show Answer {i+1}", key=f"class_ans_{i}"):
            st.write(f"✅ {q['answer']}")
    st.markdown("---")

    # Homework
    st.subheader("🏠 Homework / Tarea para Casa")
    homework_data = chapter["exercises"]["homework"]
    st.write(homework_data["description"])
    audio_player(homework_data["description"], "en", key="hw_desc_en")
    audio_player(homework_data["description"], "es", key="hw_desc_es")
    st.markdown("---")
    for i, q in enumerate(homework_data["questions"]):
        st.markdown(f"{i+1}. {q['question']}")
        if st.button(f"Show Answer {i+1}", key=f"hw_ans_{i}"):
            st.write(f"✅ {q['answer']}")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("🇺🇸🇪🇸 Let's Learn English With Gesner – Book 1 | © 2026 Teacher Gesner Deslandes")
