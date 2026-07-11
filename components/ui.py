import streamlit as st


def setup_page():
    st.set_page_config(
        page_title="AI Learning Assistant",
        page_icon=":books:",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def initialize_session():
    defaults = {
        "messages": [],
        "vector_store": None,
        "pdf_processed": False,
        "youtube_processed": False,
        "youtube_metadata": None,
        "chat_mode": "PDF Tutor",
        "generated_content": None,
        "content_generation_running": False,
        "user_name": "default",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_css():
    st.markdown(
        """
<style>
.stApp {
    background: #0E1117;
    color: white;
}

#MainMenu,
footer {
    visibility: hidden;
}

section[data-testid="stSidebar"] {
    background: #161B22;
    border-right: 1px solid #30363D;
}

h1, h2, h3 {
    color: white;
}

p {
    color: #D1D5DB;
}

.stButton > button {
    width: 100%;
    min-height: 44px;
    border-radius: 8px;
    background: #2563EB;
    color: white;
    border: none;
    font-weight: 600;
}

.stButton > button:hover {
    background: #1D4ED8;
}

.stTextInput input {
    border-radius: 8px;
}

section[data-testid="stFileUploader"] {
    border-radius: 8px;
}

.feature-card,
.status-card,
.welcome-box {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 8px;
    padding: 22px;
}

.feature-card {
    min-height: 230px;
    margin-bottom: 20px;
}

.feature-card:hover {
    border-color: #3B82F6;
}

.card-title {
    font-size: 24px;
    font-weight: 700;
    color: white;
    margin-bottom: 12px;
}

.card-text,
.metric {
    color: #D1D5DB;
    line-height: 1.7;
}

.welcome-box {
    margin: 20px 0 30px;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    color: white;
    text-align: center;
    margin-top: 15px;
}

.hero-subtitle {
    text-align: center;
    color: #9CA3AF;
    font-size: 20px;
    margin-bottom: 35px;
}

.footer {
    text-align: center;
    color: #6B7280;
    margin-top: 60px;
    padding: 20px;
}
</style>
""",
        unsafe_allow_html=True,
    )


def show_header():
    st.markdown(
        """
        <div class="hero-title">AI Learning Assistant</div>
        <div class="hero-subtitle">
            Learn smarter with PDFs, YouTube transcripts, and Gemini.
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_home():
    if len(st.session_state.messages) > 0:
        return

    show_header()

    st.markdown(
        """
        <div class="welcome-box">
            <h2>Welcome</h2>
            <p style="font-size:18px;">
                Your personal AI learning companion powered by
                <b>Gemini + LangChain + FAISS</b>.
            </p>
            <p>
                Upload study material, ask questions, or switch to General Chat
                for everyday help.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_feature_cards():
    if len(st.session_state.messages) > 0:
        return

    st.markdown("## What can I do?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="card-title">PDF Tutor</div>
                <div class="card-text">
                    Upload books, lecture notes, and research papers.
                    Ask questions and inspect source page references.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="feature-card">
                <div class="card-title">General AI Chat</div>
                <div class="card-text">
                    Explain concepts, brainstorm ideas, generate drafts,
                    and get everyday productivity help.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="card-title">YouTube Tutor</div>
                <div class="card-text">
                    Paste a YouTube URL, process its transcript, summarize
                    the video, and ask follow-up questions.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="feature-card">
                <div class="card-title">Study Material Generator</div>
                <div class="card-text">
                    Generate notes, summaries, quizzes, flashcards, and
                    interview questions from the loaded knowledge base.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("AI Model", "Gemini 2.5 Flash")

    with col2:
        st.metric("Vector DB", "FAISS")

    with col3:
        st.metric("Embeddings", "MiniLM-L6-v2")

    st.markdown("---")


def show_status():
    if len(st.session_state.messages) > 0:
        return

    st.markdown("## System Status")

    pdf_status = (
        "Processed"
        if st.session_state.get("pdf_processed", False)
        else "Not uploaded"
    )

    video_status = (
        "Processed"
        if st.session_state.get("youtube_processed", False)
        else "Not loaded"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="status-card">
                <div class="metric"><b>Status</b>: Ready</div>
                <div class="metric"><b>Model</b>: Gemini 2.5 Flash</div>
                <div class="metric"><b>Embeddings</b>: MiniLM-L6-v2</div>
                <div class="metric"><b>Framework</b>: LangChain</div>
                <div class="metric"><b>Vector Store</b>: FAISS</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="status-card">
                <div class="metric"><b>PDF Status</b>: {pdf_status}</div>
                <div class="metric"><b>YouTube Status</b>: {video_status}</div>
                <div class="metric"><b>Messages</b>: {len(st.session_state.get("messages", []))}</div>
                <div class="metric"><b>Mode</b>: {st.session_state.get("chat_mode", "PDF Tutor")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def show_suggestions():
    if len(st.session_state.messages) > 0:
        return

    st.markdown("## Try asking...")

    col1, col2 = st.columns(2)

    with col1:
        st.info("Summarize my PDF")
        st.info("Explain Chapter 2")
        st.info("Generate notes")

    with col2:
        st.info("Important interview questions")
        st.info("Explain simply")
        st.info("Give revision notes")


def show_footer():
    st.markdown("---")
    st.markdown(
        """
<div class="footer">
    <h4>AI Learning Assistant</h4>
    Built using <b>Streamlit</b> | <b>Gemini</b> | <b>LangChain</b> |
    <b>FAISS</b> | <b>HuggingFace</b>
    <br><br>
    Made by Anmol Singh
</div>
""",
        unsafe_allow_html=True,
    )
