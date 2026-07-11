"""
Prompt templates for AI Content Generation.
"""

# ==========================================================
# Notes Generator
# ==========================================================

NOTES_PROMPT = """
You are an expert teacher.

Use the retrieved context to generate well-structured study notes.

Requirements:

- Language: {language}

- Detail Level: {detail_level}

- Focus Topic: {focus_topic}

Organize the notes into:

# Title

# Introduction

# Main Concepts

# Important Definitions

# Examples

# Key Takeaways

# Summary

Use markdown formatting.

Retrieved Context:

{context}
"""


# ==========================================================
# Summary Generator
# ==========================================================

SUMMARY_PROMPT = """
You are an expert summarizer.

Summarize the retrieved content.

Language:
{language}

Length:
{detail_level}

Focus Topic:
{focus_topic}

The summary should contain:

- Main ideas

- Important concepts

- Conclusion

Context:

{context}
"""


# ==========================================================
# Quiz Generator
# ==========================================================

QUIZ_PROMPT = """
You are an AI educator.

Generate a quiz from the retrieved context.

Language:
{language}

Focus Topic:
{focus_topic}

Include:

- 10 MCQs

- 5 True/False

- 5 Short Answer Questions

Provide answers at the end.

Context:

{context}
"""


# ==========================================================
# Flashcards
# ==========================================================

FLASHCARD_PROMPT = """
Generate flashcards from the retrieved context.

Language:
{language}

Focus Topic:
{focus_topic}

Format:

Question:

Answer:

Question:

Answer:

Context:

{context}
"""


# ==========================================================
# Interview Questions
# ==========================================================

INTERVIEW_PROMPT = """
Generate interview questions from the retrieved context.

Language:
{language}

Focus Topic:
{focus_topic}

Include:

- Beginner

- Intermediate

- Advanced

Provide model answers.

Context:

{context}
"""
