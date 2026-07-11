"""
PDF Processing Component
"""

from utils.pdf_loader import load_pdf, split_documents
from utils.vector_store import create_vector_store


def process_pdf(uploaded_file):
    """
    Process an uploaded PDF and return a FAISS vector store.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        FAISS vector store
    """

    # ----------------------------------------
    # Load PDF
    # ----------------------------------------

    documents = load_pdf(uploaded_file)

    if not documents:
        raise ValueError("No readable text was found in this PDF.")

    chunks = split_documents(documents)

    # ----------------------------------------
    # Create Vector Store
    # ----------------------------------------

    vector_store = create_vector_store(chunks)

    return vector_store
