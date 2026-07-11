import streamlit as st

from components.modes import GENERAL_CHAT
from utils.chatbot import general_chat
from utils.history import add_history_entry
from utils.rag_chain import ask_question


def display_message(role: str, content: str):
    with st.chat_message(role):
        st.markdown(content)


def chat_interface(chat_mode):
    for message in st.session_state.messages:
        display_message(
            message["role"],
            message["content"],
        )

    question = st.chat_input("Ask anything...")

    if question is None:
        return

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    display_message("user", question)

    sources = []

    with st.spinner("Thinking..."):
        try:
            if chat_mode == GENERAL_CHAT:
                answer = general_chat(question)
            else:
                if st.session_state.vector_store is None:
                    st.warning("Please process a PDF or YouTube video first.")
                    return

                answer, sources = ask_question(
                    st.session_state.vector_store,
                    question,
                )

        except Exception as e:
            answer = f"Error: {str(e)}"

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    add_history_entry(
        st.session_state.get("user_name", "default"),
        "Chat",
        question[:80],
        f"Q: {question}\n\nA: {answer}",
    )

    display_message("assistant", answer)

    if chat_mode != GENERAL_CHAT and sources:
        with st.expander("Sources"):
            for source in sources:
                st.write(source.metadata)
