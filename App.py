import streamlit as st

from components.chat import chat_interface
from components.modes import PDF_TUTOR, YOUTUBE_TUTOR
from components.pdf_processor import process_pdf
from components.sidebar import sidebar
from components.ui import (
    initialize_session,
    load_css,
    setup_page,
    show_feature_cards,
    show_footer,
    show_home,
    show_status,
)
from utils.content.generator import ContentGenerator
from utils.history import add_history_entry
from utils.pdf_exporter import create_text_pdf
from utils.youtube.processor import YouTubeProcessor


def show_generated_content():
    result = st.session_state.get("generated_content")

    if result is None:
        return

    st.markdown("## Generated Study Material")
    st.caption(f"{result.content_type} | {result.detail_level} | {result.language}")
    st.markdown(result.content)

    pdf_bytes = create_text_pdf(result.title, result.content)

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "Download Markdown",
            data=result.content,
            file_name=f"{result.content_type.lower()}_study_material.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            "Download PDF",
            data=pdf_bytes,
            file_name=f"{result.content_type.lower()}_study_material.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


setup_page()
initialize_session()
load_css()

(
    uploaded_file,
    youtube_url,
    language,
    process_clicked,
    chat_mode,
    clear_chat,
    content_request,
    generate_content_clicked,
) = sidebar()


if clear_chat:
    st.session_state.messages = []
    st.session_state.vector_store = None
    st.session_state.pdf_processed = False
    st.session_state.youtube_processed = False
    st.session_state.youtube_metadata = None
    st.session_state.generated_content = None
    st.rerun()


if process_clicked:
    try:
        if chat_mode == PDF_TUTOR:
            if uploaded_file is None:
                st.warning("Please upload a PDF.")
            else:
                with st.spinner("Processing PDF..."):
                    st.session_state.vector_store = process_pdf(uploaded_file)
                    st.session_state.pdf_processed = True
                    st.session_state.youtube_processed = False
                    st.session_state.youtube_metadata = None
                    st.session_state.generated_content = None
                    st.success("PDF processed successfully!")

        elif chat_mode == YOUTUBE_TUTOR:
            if youtube_url.strip() == "":
                st.warning("Please enter a YouTube URL.")
            else:
                with st.spinner("Processing YouTube transcript..."):
                    processor = YouTubeProcessor()

                    result = processor.process_video(
                        youtube_url,
                        language,
                    )

                    st.session_state.vector_store = result.vector_store
                    st.session_state.youtube_metadata = result.metadata
                    st.session_state.youtube_processed = True
                    st.session_state.pdf_processed = False
                    st.session_state.generated_content = None
                    st.success("YouTube video processed!")

    except Exception as e:
        st.error(str(e))


if len(st.session_state.messages) == 0:
    show_home()
    show_feature_cards()
    show_status()


chat_interface(chat_mode)


if generate_content_clicked:
    if st.session_state.vector_store is None:
        st.warning("Please process a PDF or YouTube video first.")
    elif content_request is None:
        st.warning("Please choose study material options first.")
    else:
        try:
            with st.spinner("Generating study material..."):
                generator = ContentGenerator()

                result = generator.generate(
                    st.session_state.vector_store,
                    content_request,
                )

                st.session_state.generated_content = result
                add_history_entry(
                    st.session_state.get("user_name", "default"),
                    "Generated Content",
                    result.title,
                    result.content,
                )

        except Exception as e:
            st.error(str(e))


show_generated_content()

show_footer()
