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
    /* Main app background */
    .stApp {
        background: #fce4ec !important;
    }

    /* Sidebar – using proper Streamlit selectors */
    [data-testid="stSidebar"] {
        background: #f8bbd0 !important;
        border-right: 2px solid #f06292 !important;
    }

    /* Sidebar content inside */
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] .stButton button,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSelectbox div,
    [data-testid="stSidebar"] .stSelectbox option {
        color: #4a1a2a !important;
    }

    /* Sidebar headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5 {
        color: #880e4f !important;
    }

    /* Sidebar buttons – match theme */
    [data-testid="stSidebar"] .stButton button {
        background: #f06292 !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 8px 24px !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: #ec407a !important;
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(236, 64, 122, 0.3);
    }

    /* Sidebar selectbox (dropdown) */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: #fce4ec !important;
        border: 1px solid #f06292 !important;
        border-radius: 20px !important;
        color: #4a1a2a !important;
    }

    /* Sidebar radio buttons */
    [data-testid="stSidebar"] .stRadio > div {
        background: #fce4ec !important;
        border-radius: 16px !important;
        padding: 8px 12px !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #4a1a2a !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: #f8bbd0 !important;
        border-radius: 30px !important;
    }

    /* Main page headers */
    h1, h2, h3, h4, h5 {
        color: #880e4f !important;
    }

    /* Expanders */
    .stExpander {
        background: #fce4ec !important;
        border: 1px solid #f8bbd0 !important;
        border-radius: 12px !important;
    }
    .stExpander .stMarkdown {
        color: #4a1a2a !important;
    }

    /* Audio player background */
    .stAudio {
        background: #f8bbd0 !important;
        border-radius: 30px !important;
        padding: 2px 8px !important;
    }

    /* Text input fields */
    .stTextInput input {
        background: #fce4ec !important;
        border: 1px solid #f8bbd0 !important;
        border-radius: 20px !important;
        color: #4a1a2a !important;
    }
    .stTextInput input:focus {
        border-color: #f06292 !important;
    }

    /* Success/Error messages */
    .stSuccess {
        background: #a5d6a7 !important;
        color: #1e3a1e !important;
        border-radius: 20px !important;
        padding: 8px 16px !important;
    }
    .stError {
        background: #ef9a9a !important;
        color: #4a1a2a !important;
        border-radius: 20px !important;
        padding: 8px 16px !important;
    }

    /* Footer */
    .footer {
        color: #880e4f !important;
        opacity: 0.7;
        text-align: center;
        margin-top: 30px;
        font-size: 0.8rem;
    }

    /* Song lyrics styling */
    .lyrics-container {
        background: #fce4ec;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #f8bbd0;
        max-height: 500px;
        overflow-y: auto;
    }
    .lyrics-container .song-title {
        color: #880e4f;
        font-size: 1.3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 12px;
    }
    .lyrics-container .lyric-line {
        padding: 4px 0;
        font-size: 0.95rem;
        line-height: 1.6;
        border-bottom: 1px solid rgba(248, 187, 208, 0.3);
    }
    .lyrics-container .lyric-line .es {
        color: #4a1a2a;
        font-weight: 500;
    }
    .lyrics-container .lyric-line .en {
        color: #880e4f;
        font-style: italic;
        padding-left: 16px;
    }
    .lyrics-container .lyric-line:last-child {
        border-bottom: none;
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

# ---------- BOOK DATA (20 CHAPTERS WITH READINGS) ----------

# Helper to create a reading documentary for a topic
def make_reading(topic):
    english = f"This is a documentary about {topic.lower()}. Learning about {topic.lower()} is important for everyone. It helps us understand the world better. We can share our experiences and learn from each other. In this chapter, we explore {topic.lower()} from different perspectives. Remember that every day is a chance to learn something new about {topic.lower()}."
    spanish = f"Este es un documental sobre {topic.lower()}. Aprender sobre {topic.lower()} es importante para todos. Nos ayuda a entender mejor el mundo. Podemos compartir nuestras experiencias y aprender unos de otros. En este capítulo, exploramos {topic.lower()} desde diferentes perspectivas. Recuerda que cada día es una oportunidad para aprender algo nuevo sobre {topic.lower()}."
    questions = [
        {"question": f"What is the main topic of this documentary?", "answer": topic},
        {"question": "Why is learning about this topic important?", "answer": "It helps us understand the world better."},
        {"question": "What can we share with each other?", "answer": "Our experiences."},
        {"question": "What do we explore in this chapter?", "answer": f"{topic} from different perspectives."},
        {"question": "What is every day a chance for?", "answer": "To learn something new."},
        {"question": f"Who is the author of this documentary?", "answer": "Gesner Deslandes"},
        {"question": f"What is one benefit of learning about {topic.lower()}?", "answer": "It helps us understand the world better."},
        {"question": f"How can we learn about {topic.lower()}?", "answer": "By reading and exploring."},
        {"question": f"What is the title of this documentary?", "answer": f"A documentary about {topic}"},
        {"question": f"Is {topic} important? Why?", "answer": f"Yes, because it helps us understand the world better."}
    ]
    homework = [
        {"question": f"Write a sentence about {topic}.", "answer": f"I learn about {topic}."},
        {"question": f"What did you learn from this documentary?", "answer": f"I learned about {topic}."},
        {"question": f"Why should we care about {topic}?", "answer": f"Because it helps us understand the world."},
        {"question": f"Give an example of {topic} in daily life.", "answer": f"Example: {topic} is everywhere."},
        {"question": f"How can we improve our knowledge of {topic}?", "answer": f"By studying and practicing."},
        {"question": f"What is the most important aspect of {topic}?", "answer": f"Understanding its impact on our lives."},
        {"question": f"Who wrote this documentary?", "answer": "Gesner Deslandes"},
        {"question": f"What is one question you have about {topic}?", "answer": f"How can I apply {topic} in my life?"},
        {"question": f"Summarize {topic} in one sentence.", "answer": f"{topic} is important for everyone."},
        {"question": f"How does {topic} affect you personally?", "answer": f"It helps me grow and learn."}
    ]
    return {
        "title": f"Reading Documentary – {topic}",
        "english_text": english,
        "spanish_text": spanish,
        "questions": questions,
        "homework": homework
    }

# Helper to build a full chapter
def make_chapter(num, title, span_title, topic):
    conv_eng = [f"Let's talk about {title}.", f"Do you like {title.lower()}?", f"I enjoy {title.lower()} very much."]
    conv_spa = [f"Hablemos sobre {title}.", f"¿Te gusta {title.lower()}?", f"Disfruto mucho {title.lower()}."]
    vocab = [(f"word{i+1}", f"palabra{i+1}") for i in range(10)]
    idioms = [(f"Idiom {i+1}", f"Explanation {i+1}", f"Modismo {i+1}", f"Explicación {i+1}") for i in range(5)]
    pron_eng = [f"English sentence {i+1} about {title}." for i in range(10)]
    pron_spa = [f"Frase en español {i+1} sobre {title}." for i in range(10)]
    grammar = [(f"Rule {i+1}", f"Regla {i+1}") for i in range(5)]
    class_qs = [(f"Class Q{i+1}?", f"Answer{i+1}") for i in range(10)]
    hw_qs = [(f"Homework Q{i+1}?", f"Answer{i+1}") for i in range(10)]
    reading = make_reading(topic)
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
        },
        "reading": reading
    }

# Chapter topics and titles
topics = [
    "Introductions",
    "Daily Routine",
    "Family Traditions",
    "Healthy Eating Habits",
    "The Benefits of Travel",
    "My Favorite Hobby",
    "The Weather Around the World",
    "A Day at the Market",
    "Staying Healthy",
    "Different Jobs and Careers",
    "The School Experience",
    "Technology in Our Lives",
    "The Role of Media",
    "The Excitement of Sports",
    "Celebrating Festivals",
    "Protecting Our Environment",
    "Homes Around the World",
    "Fashion and Style",
    "Understanding Emotions",
    "Planning for the Future"
]
titles = [
    "Introductions",
    "Daily Routine",
    "Family",
    "Food and Drinks",
    "Travel and Transport",
    "Hobbies and Free Time",
    "Weather and Seasons",
    "Shopping",
    "Health and Body",
    "Work and Jobs",
    "Education",
    "Technology",
    "Media and Entertainment",
    "Sports",
    "Celebrations",
    "Nature and Environment",
    "House and Home",
    "Clothes and Fashion",
    "Feelings and Emotions",
    "Future Plans"
]
span_titles = [
    "Presentaciones",
    "Rutina Diaria",
    "Familia",
    "Comida y Bebidas",
    "Viajes y Transporte",
    "Pasatiempos y Tiempo Libre",
    "Clima y Estaciones",
    "Compras",
    "Salud y Cuerpo",
    "Trabajo y Empleos",
    "Educación",
    "Tecnología",
    "Medios y Entretenimiento",
    "Deportes",
    "Celebraciones",
    "Naturaleza y Medio Ambiente",
    "Casa y Hogar",
    "Ropa y Moda",
    "Sentimientos y Emociones",
    "Planes Futuros"
]

chapters = []
for i in range(20):
    ch = make_chapter(i+1, titles[i], span_titles[i], topics[i])
    chapters.append(ch)

# ---------- SONG DATA (3 Enrique Iglesias Songs) ----------
songs = {
    "Nunca Te Olvidaré": {
        "url": "https://youtu.be/pRrjt4htXlE?si=6__tGku6THjvZ2h6",
        "embed_url": "https://www.youtube.com/embed/pRrjt4htXlE",
        "lyrics": [
            {"es": "Pueden pasar tres mil años", "en": "Three thousand years may pass"},
            {"es": "Puedes besar otros labios", "en": "You may kiss other lips"},
            {"es": "Pero nunca te olvidaré", "en": "But I will never forget you"},
            {"es": "Pero nunca te olvidaré", "en": "But I will never forget you"},
            {"es": "Puedo morirme mañana", "en": "I could die tomorrow"},
            {"es": "Puede secarse mi alma", "en": "My soul could dry up"},
            {"es": "Pero nunca te olvidaré", "en": "But I will never forget you"},
            {"es": "Pero nunca te olvidaré", "en": "But I will never forget you"},
            {"es": "Más que a vivir, más que a nada", "en": "More than living, more than anything"},
            {"es": "Te quiero más que a mi vida", "en": "I love you more than my life"},
            {"es": "Y aunque pase lo que pase", "en": "And no matter what happens"},
            {"es": "Siempre te recordaré", "en": "I will always remember you"}
        ]
    },
    "Bailando": {
        "url": "https://youtu.be/4t6h6GQlG8E?si=ABC123",  # Placeholder - replace with actual URL
        "embed_url": "https://www.youtube.com/embed/4t6h6GQlG8E",
        "lyrics": [
            {"es": "Yo te miro y se me corta la respiración", "en": "I look at you and my breath catches"},
            {"es": "Cuando tú me miras se me sube el corazón", "en": "When you look at me my heart rises"},
            {"es": "Y en un silencio tu mirada dice mil palabras", "en": "And in silence your gaze says a thousand words"},
            {"es": "Ese fuego por dentro me va enloqueciendo", "en": "That fire inside me is driving me crazy"},
            {"es": "Yo quiero estar contigo, vivir contigo", "en": "I want to be with you, live with you"},
            {"es": "Bailar contigo, tener contigo", "en": "Dance with you, have with you"},
            {"es": "Una noche loca, ay besar tu boca", "en": "A crazy night, oh kiss your mouth"},
            {"es": "Ya no puedo más, ya no puedo más", "en": "I can't take it anymore, I can't take it anymore"}
        ]
    },
    "Duele el Corazón": {
        "url": "https://youtu.be/2B6O8gU6HlY?si=XYZ789",  # Placeholder - replace with actual URL
        "embed_url": "https://www.youtube.com/embed/2B6O8gU6HlY",
        "lyrics": [
            {"es": "Solo en tu boca yo quiero acabar", "en": "Only in your mouth I want to finish"},
            {"es": "Todos esos besos que te quiero dar", "en": "All those kisses I want to give you"},
            {"es": "A mí no me importa que duermas con él", "en": "I don't care if you sleep with him"},
            {"es": "Porque sé que sueñas con poderme ver", "en": "Because I know you dream of seeing me"},
            {"es": "Con él te duele el corazón", "en": "With him your heart hurts"},
            {"es": "Y conmigo te duelen los pies", "en": "And with me your feet hurt"},
            {"es": "Con él te duele el corazón", "en": "With him your heart hurts"},
            {"es": "Y conmigo te duelen los pies", "en": "And with me your feet hurt"},
            {"es": "Si te vas, yo también me voy", "en": "If you go, I'll go too"},
            {"es": "Si me das, yo también te doy", "en": "If you give me, I'll give you too"}
        ]
    }
}

# ---------- SIDEBAR: CHAPTER SELECTION ----------
st.sidebar.markdown("---")
st.sidebar.markdown("## 📚 Select Chapter")
chapter_options = [f"Chapter {ch['number']}: {ch['title']}" for ch in chapters]
selected_label = st.sidebar.selectbox("Choose a chapter:", chapter_options)
selected_idx = chapter_options.index(selected_label)
chapter = chapters[selected_idx]

# ---------- SIDEBAR: SONG SELECTION ----------
st.sidebar.markdown("---")
st.sidebar.markdown("## 🎵 Spanish Song Lyrics")
st.sidebar.markdown("*Translated into English*")
song_names = list(songs.keys())
selected_song = st.sidebar.radio("Select a song:", song_names)

# ---------- DISPLAY SELECTED CHAPTER OR SONG ----------
# Check if a song is selected (we use a session state to track)
# We'll display the song content in the main area when a song is selected from the sidebar.

# We'll use a simple approach: display song content in the main area if the user has selected a song.
# To avoid conflicts, we'll show the song content in a dedicated section.

# ---------- MAIN CONTENT: SONG DISPLAY ----------
if selected_song:
    st.header(f"🎵 {selected_song}")
    st.markdown("---")

    song = songs[selected_song]

    col1, col2 = st.columns([3, 2])

    with col1:
        # Embedded YouTube video
        st.markdown(f"""
        <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
            <iframe src="{song['embed_url']}"
                    style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
            </iframe>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Lyrics display
        st.markdown(f"""
        <div class="lyrics-container">
            <div class="song-title">🎤 {selected_song}</div>
        """, unsafe_allow_html=True)
        for line in song["lyrics"]:
            st.markdown(f"""
            <div class="lyric-line">
                <div class="es">🇪🇸 {line['es']}</div>
                <div class="en">🇺🇸 {line['en']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("🎶 Sing along and practice your Spanish pronunciation!")

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

# ---------- 6. READING DOCUMENTARY ----------
with st.expander("📄 6. Reading Documentary – Written by Gesner Deslandes", expanded=True):
    reading = chapter["reading"]
    st.markdown(f"**Title:** {reading['title']}")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("🇺🇸 **English Text**")
        st.write(reading["english_text"])
        audio_player(reading["english_text"], "en", key=f"read_en_{selected_idx}")
    with col2:
        st.markdown("🇪🇸 **Spanish Text**")
        st.write(reading["spanish_text"])
        audio_player(reading["spanish_text"], "es", key=f"read_es_{selected_idx}")
    st.markdown("---")

    # Comprehension Questions (in-app)
    st.subheader("📝 Comprehension Questions (Answer in the app)")
    for q_idx, q in enumerate(reading["questions"]):
        st.markdown(f"**{q_idx+1}. {q['question']}**")
        user_answer = st.text_input(f"Your answer:", key=f"comp_q_{selected_idx}_{q_idx}")
        if user_answer:
            if user_answer.strip().lower() == q['answer'].lower():
                st.success("✅ Correct")
            else:
                st.error("❌ Not correct")
        st.markdown("---")

    # Homework Questions (auto-graded)
    st.subheader("🏠 Homework Questions (Auto-graded)")
    for h_idx, h in enumerate(reading["homework"]):
        st.markdown(f"**{h_idx+1}. {h['question']}**")
        hw_answer = st.text_input(f"Your homework answer:", key=f"hw_q_{selected_idx}_{h_idx}")
        if hw_answer:
            if hw_answer.strip().lower() == h['answer'].lower():
                st.success("✅ Correct")
            else:
                st.error("❌ Not correct")
        st.markdown("---")

# ---------- 7. EXERCISES ----------
with st.expander("✏️ 7. Exercises / Ejercicios", expanded=True):
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
