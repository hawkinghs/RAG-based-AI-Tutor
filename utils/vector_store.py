"""
Vector Store Utilities

Responsible for:
1. Creating FAISS vector stores
2. Loading embeddings
3. Saving vector stores
4. Loading vector stores
"""

from pathlib import Path

from langchain_community.vectorstores import FAISS

from utils.embeddings import get_embeddings


# ==========================================================
# Create Vector Store
# ==========================================================

def create_vector_store(documents):
    """
    Create a FAISS vector store from LangChain documents.
    """

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    return vector_store


# ==========================================================
# Save Vector Store
# ==========================================================

def save_vector_store(
    vector_store,
    folder="vector_store"
):
    """
    Save a FAISS vector store locally.
    """

    Path(folder).mkdir(
        exist_ok=True
    )

    vector_store.save_local(folder)


# ==========================================================
# Load Vector Store
# ==========================================================

def load_vector_store(
    folder="vector_store"
):
    """
    Load a saved FAISS vector store.
    """

    embeddings = get_embeddings()

    return FAISS.load_local(
        folder,
        embeddings,
        allow_dangerous_deserialization=True
    )
