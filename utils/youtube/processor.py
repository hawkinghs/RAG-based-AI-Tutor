"""
YouTube Processing Pipeline
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.youtube.models import YouTubeProcessingResult

from utils.vector_store import create_vector_store
from utils.youtube.transcript import YouTubeTranscriptManager


class YouTubeProcessor:

    def __init__(self):

        self.transcript_manager = YouTubeTranscriptManager()

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=1000,

            chunk_overlap=200,

            separators=[

                "\n\n",

                "\n",

                ". ",

                " ",

                ""

            ]

        )

    # ---------------------------------------------------------
    # Process YouTube Video
    # ---------------------------------------------------------

    def process_video(
        self,
        youtube_url,
        language="en"
    ):

        # Fetch transcript documents
        documents = self.transcript_manager.fetch_transcript(
            youtube_url,
            language
        )

        # Split transcript
        chunks = self.splitter.split_documents(
            documents
        )

        # Create vector store
        vector_store = create_vector_store(
            chunks
        )

        # Metadata
        metadata = documents[0].metadata

        # Processing statistics
        stats = {

            "chunks": len(chunks),

            "language": language,

            "source": youtube_url,

            "video_id": metadata.get("video_id"),

            "type": "youtube"

        }

        return YouTubeProcessingResult(

    vector_store=vector_store,

    metadata=metadata,

    stats=stats

)