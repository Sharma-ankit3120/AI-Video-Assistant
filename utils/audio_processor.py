# import yt_dlp

# from pydub import AudioSegment

# import os

# DOWNLOAD_DIR = "downloads"
# os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# def download_youtube_audio(url: str) -> str:
#     output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
#     ydl_opts = {
#         "format" : "bestaudio/best",
#         "outtmpl" : output_path,
#         "ffmpeg_location": r"C:\ffmpeg\ffmpeg-8.1.2-essentials_build\bin",
#         "postprocessors" : [{
#             "key" : "FFmpegExtractAudio",
#             "preferredcodec" : "wav",
#             "preferredquality" : "192",
#         }], "quiet" : True
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(url, download=True)
#         filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
#         return filename
    
    
# def convert_to_wav(input_path: str) -> str:
#     """Convert an audio/video file to WAV format using pydub."""
#     output_path = os.path.splitext(input_path)[0] + "_converted.wav"
#     audio = AudioSegment.from_file(input_path)
#     audio = audio.set_channels(1).set_frame_rate(16000)  # Convert to mono
#     audio.export(output_path, format="wav")
#     return output_path



# def chunk_audio(wav_path:str, chunk_minutes:int =10) -> list:
#     """Chunk a WAV file into smaller segments of specified duration in minutes."""
#     audio = AudioSegment.from_wav(wav_path)
#     chunk_ms = chunk_minutes * 60 * 1000  # Convert minutes to milliseconds
#     chunks = []
    
#     for i,start  in enumerate(range(0, len(audio), chunk_ms)):
#         chunk = audio[start:start + chunk_ms]
#         chunk_path = f"{wav_path}_chunk_{i}.wav"
#         chunk.export(chunk_path, format="wav")
#         chunks.append(chunk_path)
    
#     return chunks



# def process_input(source:str)->list:
#     if source.startswith("http://") or source.startswith("https://"):
#         print(f"Detected YouTube URL. Downloading audio")
#         wav_path = download_youtube_audio(source)

#     else:
#         print(f"Detected local file. Converting to WAV")
#         wav_path = convert_to_wav(source)

#     print(f"Chunking audio into segments")
#     chunks = chunk_audio(wav_path)
#     print(f"Audio Created - {len(chunks)} chunk(S) created.")
#     return chunks

import yt_dlp
from pydub import AudioSegment
import os

from core.transcriber import detect_language

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format" : "bestaudio/best",
        "outtmpl" : output_path,
        "ffmpeg_location": r"C:\ffmpeg\ffmpeg-8.1.2-essentials_build\bin",
        "postprocessors" : [{
            "key" : "FFmpegExtractAudio",
            "preferredcodec" : "wav",
            "preferredquality" : "192",
        }], "quiet" : True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
        return filename
    

def convert_to_wav(input_path: str) -> str:
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, source_lang: str = "en") -> list:
    audio = AudioSegment.from_wav(wav_path)

    # 30 seconds for Hindi (needs small chunks for speed)
    # 10 minutes for English (big chunks are fine)
    if source_lang == "hi":
        chunk_ms = 30 * 1000
        print("Hindi detected → 30 second chunks")
    else:
        chunk_ms = 10 * 60 * 1000
        print("English detected → 10 minute chunks")

    chunks = []
    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start:start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list:  # ✅ returns only chunks now, not tuple
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV")
        wav_path = convert_to_wav(source)

    # detect language from first 30 seconds before chunking
    print("Detecting language...")
    sample = AudioSegment.from_wav(wav_path)[:30000]
    sample_path = wav_path + "_sample.wav"
    sample.export(sample_path, format="wav")
    detected_lang = detect_language(sample_path)
    os.remove(sample_path)

    print("Chunking audio into segments")
    chunks = chunk_audio(wav_path, source_lang=detected_lang)
    print(f"Audio Created - {len(chunks)} chunk(S) created.")

    return chunks  # ✅ just chunks, no lang needed anymore