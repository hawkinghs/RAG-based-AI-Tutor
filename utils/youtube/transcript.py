from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
)

from langchain_core.documents import Document

from utils.youtube.helpers import extract_video_id


class YouTubeTranscriptManager:

    def __init__(self):

        self.api = YouTubeTranscriptApi()

    # ---------------------------------------------------
    # Language Mapping
    # ---------------------------------------------------

    LANGUAGE_MAP = {

        "en": [
            "en",
            "en-IN",
            "en-US",
            "en-GB",
        ],

        "hi": [
            "hi",
        ],

        "es": [
            "es",
        ],

        "fr": [
            "fr",
        ],

        "de": [
            "de",
        ],

        "ja": [
            "ja",
        ],

    }

    # ---------------------------------------------------
    # Fetch Transcript
    # ---------------------------------------------------

    def fetch_transcript(
        self,
        url,
        language="en",
    ):

        video_id = extract_video_id(url)

        transcript_list = self.api.list(video_id)

        preferred_languages = self.LANGUAGE_MAP.get(
            language,
            [language],
        )

        transcript = None

        # -----------------------------------------
        # Try preferred language
        # -----------------------------------------

        for lang in preferred_languages:

            try:

                transcript = transcript_list.find_transcript(
                    [lang]
                )

                break

            except NoTranscriptFound:

                continue

        # -----------------------------------------
        # Fallback
        # -----------------------------------------

        if transcript is None:

            available = list(transcript_list)

            if len(available) == 0:

                raise NoTranscriptFound(
                    video_id,
                    [language],
                    transcript_list,
                )

            transcript = available[0]

        # -----------------------------------------
        # Fetch
        # -----------------------------------------

        transcript_data = transcript.fetch()

        text = "\n".join(

            chunk.text

            for chunk in transcript_data

        )

        return [

            Document(

                page_content=text,

                metadata={

                    "video_id": video_id,

                    "language": transcript.language_code,

                    "is_generated": transcript.is_generated,

                },

            )

        ]

    def get_available_languages(self, url):
        """
        Return available transcript languages for a YouTube URL.
        """

        video_id = extract_video_id(url)
        transcript_list = self.api.list(video_id)

        return [
            {
                "language": transcript.language,
                "language_code": transcript.language_code,
                "is_generated": transcript.is_generated,
            }
            for transcript in transcript_list
        ]
