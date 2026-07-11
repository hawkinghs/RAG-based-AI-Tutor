from utils.llm import get_llm


def general_chat(question: str) -> str:
    """
    General AI Chat using Gemini.
    """

    llm = get_llm()

    response = llm.invoke(question)

    return response.content