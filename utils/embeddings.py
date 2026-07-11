import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource
def get_embeddings():
    """
    Load and cache the HuggingFace embedding model.
    """

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={
            "device": "cpu",
        },
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )