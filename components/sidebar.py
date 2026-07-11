import streamlit as st

from components.modes import GENERAL_CHAT, MODE_OPTIONS, PDF_TUTOR, YOUTUBE_TUTOR
from utils.content.models import ContentGenerationRequest
from utils.history import load_history


def sidebar():
    with st.sidebar:
        st.title("AI Learning Assistant")
        st.caption("Learn from PDFs, YouTube and AI")

        st.divider()

        user_name = st.text_input(
            "User Name",
            value=st.session_state.get("user_name", "default"),
        ).strip() or "default"
        st.session_state.user_name = user_name

        with st.expander("History"):
            history = load_history(user_name)

            if not history:
                st.caption("No history yet.")
            else:
                for item in history[:10]:
                    st.caption(f"{item.get('created_at', '')} | {item.get('type', '')}")
                    st.write(item.get("title", "Untitled"))

        chat_mode = st.radio(
            "Choose Mode",
            MODE_OPTIONS,
        )

        st.session_state.chat_mode = chat_mode

        st.divider()

        uploaded_file = None
        youtube_url = ""
        language = "en"
        process_clicked = False

        if chat_mode == PDF_TUTOR:
            st.subheader("Upload PDF")

            uploaded_file = st.file_uploader(
                "Choose a PDF",
                type=["pdf"],
            )

            process_clicked = st.button(
                "Process PDF",
                use_container_width=True,
            )

        elif chat_mode == YOUTUBE_TUTOR:
            st.subheader("YouTube")

            youtube_url = st.text_input("Paste YouTube URL")

            languages = {
                "English": "en",
                "Hindi": "hi",
                "Spanish": "es",
                "French": "fr",
                "German": "de",
                "Japanese": "ja",
            }

            selected_language = st.selectbox(
                "Transcript Language",
                list(languages.keys()),
            )

            language = languages[selected_language]

            process_clicked = st.button(
                "Process Video",
                use_container_width=True,
            )

        else:
            st.info("Chat directly with Gemini.\n\nNo document required.")

        st.divider()

        st.subheader("System Status")

        if st.session_state.get("pdf_processed", False):
            st.success("PDF ready")

        elif st.session_state.get("youtube_processed", False):
            st.success("Video ready")

            metadata = st.session_state.get("youtube_metadata")

            if metadata:
                st.caption(f"Video ID: {metadata.get('video_id', '-')}")
                st.caption(f"Language: {metadata.get('language', '-')}")

        else:
            st.warning("No knowledge base loaded")

        content_request = None
        generate_content_clicked = False

        if (
            st.session_state.get("pdf_processed", False)
            or st.session_state.get("youtube_processed", False)
        ):
            st.divider()
            st.subheader("Study Material")

            content_type = st.selectbox(
                "Content Type",
                [
                    "Notes",
                    "Summary",
                    "Quiz",
                    "Flashcards",
                    "Interview",
                ],
            )

            detail_level = st.radio(
                "Detail Level",
                [
                    "Short",
                    "Moderate",
                    "Detailed",
                ],
                horizontal=True,
            )

            focus_topic = st.text_input(
                "Topic (Optional)",
                placeholder="Example: Backpropagation",
            )

            output_format = st.selectbox(
                "Export Format",
                [
                    "Markdown",
                    "PDF",
                ],
            )

            generate_content_clicked = st.button(
                "Generate",
                use_container_width=True,
            )

            content_request = ContentGenerationRequest(
                content_type=content_type,
                detail_level=detail_level,
                language=selected_language if chat_mode == YOUTUBE_TUTOR else "English",
                output_format=output_format,
                focus_topic=focus_topic,
            )

        st.divider()

        clear_chat = st.button(
            "Clear Chat",
            use_container_width=True,
        )

    return (
        uploaded_file,
        youtube_url,
        language,
        process_clicked,
        chat_mode,
        clear_chat,
        content_request,
        generate_content_clicked,
    )
