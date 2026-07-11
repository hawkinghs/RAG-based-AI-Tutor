"""
Data models used by the YouTube module.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class YouTubeProcessingResult:
    """
    Result returned after processing a YouTube video.
    """

    vector_store: Any

    metadata: Dict

    stats: Dict