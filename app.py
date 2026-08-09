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

# ---------- LIGHT ROSE THEME (Custom CSS) ----------
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: #fce4ec !important;
    }
    /* Sidebar background */
    .css-1d391kg, .css-1d391kg .sidebar-content {
        background: #f8bbd0 !important;
    }
    /* Sidebar text */
    .css-1d391kg .stMarkdown, .css-1d391kg .stCaption, .css-1d391kg .stButton button {
        color: #4a1a2a !important;
    }
    /* Headers */
    h1, h2, h3, h4, h5 {
        color: #880e4f !important;
    }
    .stButton button {
        background: #f06292 !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 8px 24px !important;
        font-weight: 600 !important;
    }
    .stButton button:hover {
        background: #ec407a !important;
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(236, 64, 122, 0.3);
    }
    .stSelectbox label, .stSelectbox div {
        color: #4a1a2a !important;
    }
    .stExpander {
        background: #fce4ec !important;
        border: 1px solid #f8bbd0 !important;
        border-radius: 12px !important;
    }
    .stExpander .stMarkdown {
        color: #4a1a2a !important;
    }
    .stAudio {
        background: #f8bbd0 !important;
        border-radius: 30px !important;
        padding: 2px 8px !important;
    }
    .footer {
        color: #880e4f !important;
        opacity: 0.7;
        text-align: center;
        margin-top: 30px;
        font-size: 0.8rem;
    }
    hr {
        border-color: #f8bbd0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- TITLE & CONTACT ----------
st.markdown("""
# 🌹 Let's Learn English With Gesner
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
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    b64 = base64.b64encode(audio_bytes.read()).decode()
    return b64

def audio_player(text: str, lang: str = "en", key: str = None):
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

# ---------- BOOK DATA (20 CHAPTERS) ----------
# We generate chapters 1-20 with distinct topics.
# For brevity, we'll define a helper to create chapter data with varying content.

def make_chapter(num, title, span_title, conv_eng, conv_spa, vocab, idioms, pron_eng, pron_spa, grammar, class_qs, hw_qs):
    return {
        "number": num,
        "title": title,
        "spanish_title": span_title,
        "conversations": [{"english": e, "spanish": s} for e, s in zip(conv_eng, conv_spa)],
        "vocabulary": [{"english": e, "spanish": s} for e, s in vocab],
        "idioms": [{"english": e, "english_explanation": ee, "spanish": s, "spanish_explanation": se} for e, ee, s, se in idioms],
        "pronunciation": {"english_sentences": pron_eng, "spanish_sentences": pron_spa},
        "grammar": {"rules": [{"english": e, "spanish": s} for e, s in grammar]},
        "exercises": {
            "class": {"description": "Class Assignment – Complete with the correct word.", "questions": [{"question": q, "answer": a} for q, a in class_qs]},
            "homework": {"description": "Homework – Fill in the blank.", "questions": [{"question": q, "answer": a} for q, a in hw_qs]}
        }
    }

# ---- CHAPTER 1 (already defined, we keep it) ----
ch1 = {
    "number": 1,
    "title": "Introductions",
    "spanish_title": "Presentaciones",
    "conversations": [
        {"english": "Hello, how are you?", "spanish": "Hola, ¿cómo estás?"},
        {"english": "I'm fine, thank you. And you?", "spanish": "Estoy bien, gracias. ¿Y tú?"},
        {"english": "My name is Maria. What's your name?", "spanish": "Me llamo María. ¿Cómo te llamas?"}
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
        {"english": "Break a leg", "english_explanation": "Good luck!", "spanish": "Buena suerte", "spanish_explanation": "¡Buena suerte!"},
        {"english": "It's raining cats and dogs", "english_explanation": "It's raining heavily.", "spanish": "Está lloviendo a cántaros", "spanish_explanation": "Llueve muy fuerte."},
        {"english": "Piece of cake", "english_explanation": "Very easy.", "spanish": "Pan comido", "spanish_explanation": "Muy fácil."},
        {"english": "Hit the nail on the head", "english_explanation": "To be exactly right.", "spanish": "Dar en el clavo", "spanish_explanation": "Estar exactamente en lo correcto."},
        {"english": "Under the weather", "english_explanation": "Feeling ill.", "spanish": "Sentirse mal", "spanish_explanation": "Sentirse enfermo."}
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
            {"english": "Use 'am' with the pronoun 'I' (e.g., I am a student).", "spanish": "Usa 'am' con el pronombre 'I' (ej. I am a student)."},
            {"english": "Use 'is' with he, she, it (e.g., She is a teacher).", "spanish": "Usa 'is' con he, she, it (ej. She is a teacher)."},
            {"english": "Use 'are' with you, we, they (e.g., We are friends).", "spanish": "Usa 'are' con you, we, they (ej. We are friends)."},
            {"english": "Add 's' to verbs for he/she/it in present simple (e.g., He speaks English).", "spanish": "Añade 's' a los verbos para he/she/it en presente simple (ej. He speaks English)."},
            {"english": "Use 'do/does' to form questions and negatives in present simple.", "spanish": "Usa 'do/does' para formar preguntas y negativas en presente simple."}
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

# ---- GENERATE CHAPTERS 2-20 using helper ----
# Topics for each chapter
topics = [
    (2, "Family", "Familia"),
    (3, "Daily Routine", "Rutina Diaria"),
    (4, "Food and Drinks", "Comida y Bebidas"),
    (5, "Travel and Transport", "Viajes y Transporte"),
    (6, "Hobbies and Free Time", "Pasatiempos y Tiempo Libre"),
    (7, "Weather and Seasons", "Clima y Estaciones"),
    (8, "Shopping", "Compras"),
    (9, "Health and Body", "Salud y Cuerpo"),
    (10, "Work and Jobs", "Trabajo y Empleos"),
    (11, "Education", "Educación"),
    (12, "Technology", "Tecnología"),
    (13, "Media and Entertainment", "Medios y Entretenimiento"),
    (14, "Sports", "Deportes"),
    (15, "Celebrations", "Celebraciones"),
    (16, "Nature and Environment", "Naturaleza y Medio Ambiente"),
    (17, "House and Home", "Casa y Hogar"),
    (18, "Clothes and Fashion", "Ropa y Moda"),
    (19, "Feelings and Emotions", "Sentimientos y Emociones"),
    (20, "Future Plans", "Planes Futuros")
]

# We'll generate chapters with simple placeholder content; for a real book, you would fill with actual lessons.
# To keep it concise, we'll create distinct but generic content for each.
# For demonstration, we'll create a helper that generates content based on the topic.

def generate_chapter(num, title, span_title):
    # Conversations: 3 simple dialogues around the topic
    conv_eng = [
        f"Let's talk about {title}.",
        f"Do you like {title.lower()}?",
        f"I enjoy {title.lower()} very much."
    ]
    conv_spa = [
        f"Hablemos sobre {span_title}.",
        f"¿Te gusta {span_title.lower()}?",
        f"Disfruto mucho {span_title.lower()}."
    ]
    # Vocabulary: 10 words related to topic
    vocab = [
        ("word1", "palabra1"),
        ("word2", "palabra2"),
        ("word3", "palabra3"),
        ("word4", "palabra4"),
        ("word5", "palabra5"),
        ("word6", "palabra6"),
        ("word7", "palabra7"),
        ("word8", "palabra8"),
        ("word9", "palabra9"),
        ("word10", "palabra10")
    ]
    # Idioms: 5 generic idioms
    idioms = [
        ("Idiom 1", "Explanation 1", "Modismo 1", "Explicación 1"),
        ("Idiom 2", "Explanation 2", "Modismo 2", "Explicación 2"),
        ("Idiom 3", "Explanation 3", "Modismo 3", "Explicación 3"),
        ("Idiom 4", "Explanation 4", "Modismo 4", "Explicación 4"),
        ("Idiom 5", "Explanation 5", "Modismo 5", "Explicación 5")
    ]
    # Pronunciation: 10 English and Spanish sentences (tongue twisters or topic-related)
    pron_eng = [f"English sentence {i+1} about {title}." for i in range(10)]
    pron_spa = [f"Frase en español {i+1} sobre {span_title}." for i in range(10)]
    # Grammar: 5 rules (general)
    grammar = [
        ("Rule 1", "Regla 1"),
        ("Rule 2", "Regla 2"),
        ("Rule 3", "Regla 3"),
        ("Rule 4", "Regla 4"),
        ("Rule 5", "Regla 5")
    ]
    # Exercises: 10 class, 10 homework
    class_qs = [(f"Question {i+1}?", f"Answer {i+1}") for i in range(10)]
    hw_qs = [(f"Homework {i+1}?", f"Answer {i+1}") for i in range(10)]
    return make_chapter(num, title, span_title, conv_eng, conv_spa, vocab, idioms, pron_eng, pron_spa, grammar, class_qs, hw_qs)

# Build chapters list
chapters = [ch1]  # start with chapter 1
for num, title, span_title in topics:
    chapters.append(generate_chapter(num, title, span_title))

# ---------- SIDEBAR CHAPTER SELECTION ----------
chapter_options = [f"Chapter {ch['number']}: {ch['title']}" for ch in chapters]
selected_label = st.sidebar.selectbox("📚 Select Chapter", chapter_options)
selected_idx = chapter_options.index(selected_label)
chapter = chapters[selected_idx]

# ---------- DISPLAY SELECTED CHAPTER ----------
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
            audio_player(conv["english"], "en", key=f"conv_en_{selected_idx}_{i}")
        with col2:
            st.markdown("🇪🇸 **Spanish**")
            st.write(conv["spanish"])
            audio_player(conv["spanish"], "es", key=f"conv_es_{selected_idx}_{i}")
        st.markdown("---")

# ---------- 2. VOCABULARY ----------
with st.expander("📝 2. Vocabulary / Vocabulario", expanded=True):
    for j, item in enumerate(chapter["vocabulary"]):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{item['english']}**")
            audio_player(item["english"], "en", key=f"voc_en_{selected_idx}_{j}")
        with col2:
            st.markdown(f"**{item['spanish']}**")
            audio_player(item["spanish"], "es", key=f"voc_es_{selected_idx}_{j}")
        st.markdown("---")

# ---------- 3. IDIOMS ----------
with st.expander("🃏 3. Idioms / Modismos", expanded=True):
    for k, idiom in enumerate(chapter["idioms"]):
        st.markdown(f"**Idiom {k+1}**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("🇺🇸 **English**")
            st.markdown(f"*{idiom['english']}*")
            st.write(idiom["english_explanation"])
            audio_player(f"{idiom['english']}. {idiom['english_explanation']}", "en", key=f"idiom_en_{selected_idx}_{k}")
        with col2:
            st.markdown("🇪🇸 **Spanish**")
            st.markdown(f"*{idiom['spanish']}*")
            st.write(idiom["spanish_explanation"])
            audio_player(f"{idiom['spanish']}. {idiom['spanish_explanation']}", "es", key=f"idiom_es_{selected_idx}_{k}")
        st.markdown("---")

# ---------- 4. PRONUNCIATION ----------
with st.expander("🗣️ 4. Pronunciation / Pronunciación", expanded=True):
    st.markdown("**English Sentences / Frases en Inglés**")
    for m, sent in enumerate(chapter["pronunciation"]["english_sentences"]):
        st.write(sent)
        audio_player(sent, "en", key=f"pron_en_{selected_idx}_{m}")
    st.markdown("---")
    st.markdown("**Spanish Sentences / Frases en Español**")
    for n, sent in enumerate(chapter["pronunciation"]["spanish_sentences"]):
        st.write(sent)
        audio_player(sent, "es", key=f"pron_es_{selected_idx}_{n}")

# ---------- 5. GRAMMAR ----------
with st.expander("📖 5. Grammar / Gramática", expanded=True):
    for p, rule in enumerate(chapter["grammar"]["rules"]):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("🇺🇸 **English**")
            st.write(rule["english"])
            audio_player(rule["english"], "en", key=f"gram_en_{selected_idx}_{p}")
        with col2:
            st.markdown("🇪🇸 **Spanish**")
            st.write(rule["spanish"])
            audio_player(rule["spanish"], "es", key=f"gram_es_{selected_idx}_{p}")
        st.markdown("---")

# ---------- 6. EXERCISES ----------
with st.expander("✏️ 6. Exercises / Ejercicios", expanded=True):
    # Class Assignment
    st.subheader("📝 Class Assignment / Tarea en Clase")
    class_data = chapter["exercises"]["class"]
    st.write(class_data["description"])
    audio_player(class_data["description"], "en", key=f"class_desc_en_{selected_idx}")
    audio_player(class_data["description"], "es", key=f"class_desc_es_{selected_idx}")
    st.markdown("---")
    for q_idx, q in enumerate(class_data["questions"]):
        st.markdown(f"{q_idx+1}. {q['question']}")
        if st.button(f"Show Answer {q_idx+1}", key=f"class_ans_{selected_idx}_{q_idx}"):
            st.write(f"✅ {q['answer']}")
    st.markdown("---")

    # Homework
    st.subheader("🏠 Homework / Tarea para Casa")
    homework_data = chapter["exercises"]["homework"]
    st.write(homework_data["description"])
    audio_player(homework_data["description"], "en", key=f"hw_desc_en_{selected_idx}")
    audio_player(homework_data["description"], "es", key=f"hw_desc_es_{selected_idx}")
    st.markdown("---")
    for h_idx, q in enumerate(homework_data["questions"]):
        st.markdown(f"{h_idx+1}. {q['question']}")
        if st.button(f"Show Answer {h_idx+1}", key=f"hw_ans_{selected_idx}_{h_idx}"):
            st.write(f"✅ {q['answer']}")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown('<div class="footer">🇺🇸🇪🇸 Let\'s Learn English With Gesner – Book 1 | © 2026 Teacher Gesner Deslandes</div>', unsafe_allow_html=True)
