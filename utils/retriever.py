def retrieve_documents(vector_store, query, k=10):
    """
    Retrieve the most relevant documents from the user's
    in-memory vector store.
    """

    documents = vector_store.similarity_search(
        query=query,
        k=k
    )

    return documents