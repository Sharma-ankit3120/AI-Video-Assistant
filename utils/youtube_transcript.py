from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from youtube_transcript_api._errors import NoTranscriptFound
import re
import streamlit as st

def get_video_id(url: str) -> str:
    patterns = [
        r"v=([^&]+)",
        r"youtu\.be/([^?]+)",
        r"embed/([^?]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from URL: {url}")


def fetch_transcript(url: str) -> str:
    video_id = get_video_id(url)
    print(f"Fetching transcript for video: {video_id}")

    # ✅ use webshare proxy to bypass YouTube cloud IP block
    proxy_config = WebshareProxyConfig(
        proxy_username=st.secrets["PROXY_USERNAME"],
        proxy_password=st.secrets["PROXY_PASSWORD"],
    )

    ytt = YouTubeTranscriptApi(proxy_config=proxy_config)

    try:
        fetched = ytt.fetch(video_id, languages=["en"])
        print("Found English transcript")

    except NoTranscriptFound:
        try:
            fetched = ytt.fetch(video_id, languages=["hi"])
            print("Found Hindi transcript")

        except NoTranscriptFound:
            transcript_list = ytt.list(video_id)
            transcript_obj = transcript_list.find_transcript(
                [t.language_code for t in transcript_list]
            )
            fetched = transcript_obj.translate("en").fetch()
            print("Translated transcript to English")

    full_text = " ".join([snippet.text for snippet in fetched])
    return full_text