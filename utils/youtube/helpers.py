"""
Utility functions for YouTube processing.
"""

import re
from urllib.parse import urlparse, parse_qs


# ---------------------------------------------------------
# Validate YouTube URL
# ---------------------------------------------------------

def is_valid_youtube_url(url: str) -> bool:
    """
    Check whether a URL belongs to YouTube.
    """

    youtube_domains = [
        "youtube.com",
        "www.youtube.com",
        "youtu.be",
        "m.youtube.com"
    ]

    try:

        parsed = urlparse(url.strip())

        return parsed.netloc in youtube_domains

    except Exception:

        return False


# ---------------------------------------------------------
# Extract Video ID
# ---------------------------------------------------------

def extract_video_id(url: str) -> str:
    """
    Extract the 11-character YouTube video ID.

    Supports:
    - youtube.com/watch?v=
    - youtu.be/
    - youtube.com/embed/
    - youtube.com/shorts/
    """

    if not is_valid_youtube_url(url):
        raise ValueError("Invalid YouTube URL.")

    parsed = urlparse(url.strip())

    # Short URL
    if parsed.netloc == "youtu.be":

        video_id = parsed.path.strip("/").split("/")[0]

        if len(video_id) == 11:
            return video_id

        raise ValueError("Unable to extract video ID.")

    # Normal watch URL
    if "watch" in parsed.path:

        video_id = parse_qs(parsed.query).get("v", [""])[0]

        if len(video_id) == 11:
            return video_id

        raise ValueError("Unable to extract video ID.")

    # Shorts
    if "/shorts/" in parsed.path:

        video_id = parsed.path.split("/shorts/")[1].split("/")[0]

        if len(video_id) == 11:
            return video_id

        raise ValueError("Unable to extract video ID.")

    # Embed
    if "/embed/" in parsed.path:

        video_id = parsed.path.split("/embed/")[1].split("/")[0]

        if len(video_id) == 11:
            return video_id

        raise ValueError("Unable to extract video ID.")

    raise ValueError("Unable to extract video ID.")


# ---------------------------------------------------------
# Sanitize Filename
# ---------------------------------------------------------

def sanitize_filename(name: str) -> str:
    """
    Remove characters that are invalid in Windows filenames.
    """

    return re.sub(
        r'[<>:"/\\\\|?*]',
        "",
        name
    ).strip()
