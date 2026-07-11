"""
Modern RAG Utilities (LangChain LCEL)

Used by:
- PDF Chat
- YouTube Chat
- Notes Generator
- Quiz Generator
- Flashcards
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from utils.llm import get_llm


# ==========================================================
# Retrieve Context
# ==========================================================

def retrieve_context(
    vector_store,
    query,
    k=4,
):
    """
    Retrieve relevant documents from the vector database.
    """

    retriever = vector_store.as_retriever(
        search_kwargs={"k": k}
    )

    return retriever.invoke(query)


# ==========================================================
# Ask Question
# ==========================================================

def ask_question(
    vector_store,
    question,
):
    """
    Ask questions over the vector database.
    """

    docs = retrieve_context(
        vector_store,
        question,
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are an expert AI tutor.

Answer ONLY using the provided context.

If the answer is not present in the context,
say that you don't know.

Context:
{context}

Question:
{question}
"""
    )

    llm = get_llm()

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return answer, docs