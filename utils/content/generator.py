"""
Universal AI Content Generator

Supports:

- Notes
- Summary
- Quiz
- Flashcards
- Interview Questions
"""

from utils.content.models import (
    ContentGenerationRequest,
    ContentGenerationResult,
)

from utils.content.prompts import (
    NOTES_PROMPT,
    SUMMARY_PROMPT,
    QUIZ_PROMPT,
    FLASHCARD_PROMPT,
    INTERVIEW_PROMPT,
)

from utils.rag_chain import retrieve_context
from utils.llm import get_llm


class ContentGenerator:

    def __init__(self):

        self.llm = get_llm()

    # --------------------------------------------------------
    # Prompt Selector
    # --------------------------------------------------------

    def _get_prompt(
        self,
        content_type,
    ):

        prompts = {

            "Notes": NOTES_PROMPT,

            "Summary": SUMMARY_PROMPT,

            "Quiz": QUIZ_PROMPT,

            "Flashcards": FLASHCARD_PROMPT,

            "Interview": INTERVIEW_PROMPT,

        }

        return prompts[content_type]

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    def generate(
        self,
        vector_store,
        request: ContentGenerationRequest,
    ):
        if vector_store is None:
            raise ValueError("Please process a PDF or YouTube video first.")

        query = request.focus_topic.strip() or request.content_type

        # ----------------------------------------
        # Retrieve Context
        # ----------------------------------------

        documents = retrieve_context(

            vector_store,

            query,

            k=8,

        )

        context = "\n\n".join(

            doc.page_content

            for doc in documents

        )

        # ----------------------------------------
        # Prompt
        # ----------------------------------------

        prompt = self._get_prompt(

            request.content_type

        )

        prompt = prompt.format(

            language=request.language,

            detail_level=request.detail_level,

            context=context,

            focus_topic=request.focus_topic.strip() or "the full retrieved material",

        )

        # ----------------------------------------
        # Gemini
        # ----------------------------------------

        response = self.llm.invoke(

            prompt

        )

        # ----------------------------------------
        # Return
        # ----------------------------------------

        return ContentGenerationResult(

            title=f"{request.content_type}",

            content=response.content,

            content_type=request.content_type,

            detail_level=request.detail_level,

            language=request.language,

            output_format=request.output_format,

        )
