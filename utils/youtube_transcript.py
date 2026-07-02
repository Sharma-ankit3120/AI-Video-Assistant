from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url: str) -> str:
    """Extract video ID from YouTube URL"""
    patterns = [
        r"v=([^&]+)",           # standard ?v=
        r"youtu\.be/([^?]+)",   # short URL
        r"embed/([^?]+)",       # embed URL
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from URL: {url}")


def fetch_transcript(url: str) -> str:
    """
    Fetch transcript directly from YouTube subtitles.
    Tries English first, then Hindi (translated to English), then any available.
    No audio download needed — works on Streamlit Cloud.
    """
    video_id = get_video_id(url)
    print(f"Fetching transcript for video: {video_id}")

    try:
        # Try English transcript first
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        print("Found English transcript")

    except Exception:
        try:
            # Try Hindi transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["hi"])
            print("Found Hindi transcript")

        except Exception:
            # Get whatever is available
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript_obj = transcript_list.find_transcript(
                [t.language_code for t in transcript_list]
            )
            # translate to English if not already
            transcript = transcript_obj.translate("en").fetch()
            print(f"Translated transcript to English")

    # join all text segments
    full_text = " ".join([entry["text"] for entry in transcript])
    return full_text