"""
Data models for AI Content Generation.

These models are shared by:
- Notes Generator
- Summary Generator
- Quiz Generator
- Flashcards
- Interview Questions
"""

from dataclasses import dataclass
from typing import Optional


# ==========================================================
# User Request
# ==========================================================


@dataclass
class ContentGenerationRequest:

    content_type: str

    detail_level: str = "Moderate"

    language: str = "English"

    output_format: str = "PDF"

    focus_topic: str = ""

# ==========================================================
# Generated Result
# ==========================================================

@dataclass
class ContentGenerationResult:
    """
    Represents generated content.
    """

    title: str

    content: str

    content_type: str

    detail_level: str

    language: str

    output_format: str

    source_type: Optional[str] = None

    source_name: Optional[str] = None