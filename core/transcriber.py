# # Mainly the whisper is used to transcribe the audio files into text. It is a powerful tool that can handle various audio formats and languages, making it suitable for a wide range of

# # secondly we will use it to change the language from hindi to english 



# # from more_itertools import one
# # import whisper 
# # import os



# # WHISPER_MODEL = "small"


# # _model = None

# # def load_model():

# #     global _model

# #     if _model is None:
# #          print("Loading Whisper model...")
# #          _model = whisper.load_model(WHISPER_MODEL)  
# #          print("Whisper model loaded successfully.")

# #     return _model

# # def transcribe_chunk(chunk_path : str, translate: bool = False) -> str:
# #     model = load_model()

# #     task = "translate" if translate else "transcribe"

# #     result = model.transcribe(chunk_path, task=task)

# #     return result['text']

# # def transcribe_all(chunks: list, translate: bool = False) -> str:
# #     full_transcript = ""

# #     for i , chunk in enumerate(chunks):
# #         print(f"Transcribing chunk {i+1}")
# #         transcript = transcribe_chunk(chunk, translate=translate)
# #         full_transcript += transcript + " "

# #     print("Transcription completed.")

# #     return full_transcript


# # ✅ CHANGE 1: replaced `import whisper` with `faster_whisper`
# from faster_whisper import WhisperModel
# import torch
# import os

# # ✅ CHANGE 2: limit CPU threads (your RAM is at 92%)
# torch.set_num_threads(2)

# # ✅ CHANGE 3: small + int8 instead of medium (3x faster on your Intel GPU)
# _model = None

# def load_model():
#     global _model
#     if _model is None:
#         print("Loading Whisper model...")
#         _model = WhisperModel(
#             "small",
#             device="cpu",
#             compute_type="int8",  # quantized = less RAM, faster
#             cpu_threads=2,
#             num_workers=1,
#         )
#         print("Whisper model loaded.")
#     return _model


# def detect_language(chunk_path: str) -> str:
#     """Auto-detect the spoken language in an audio chunk."""
#     model = load_model()
#     # ✅ CHANGE 4: faster_whisper detect language API is different
#     segments, info = model.transcribe(chunk_path, beam_size=1)
#     detected = info.language
#     confidence = info.language_probability
#     print(f"Detected language: {detected} (confidence: {confidence:.2f})")
#     return detected


# def transcribe_chunk(chunk_path: str, translate: bool = False, source_lang: str = None) -> str:
#     model = load_model()

#     if source_lang is None:
#         source_lang = detect_language(chunk_path)

#     # ✅ CHANGE 5: faster_whisper uses segments iterator, not result['text']
#     task = "translate" if translate else "transcribe"

#     if source_lang == "hi":
#         print("  Transcribing Hindi...")
#         segments, _ = model.transcribe(
#             chunk_path,
#             task=task,
#             language="hi",
#             beam_size=1,        # ✅ CHANGE 6: was 5, now 1 (3x faster)
#             vad_filter=True,    # ✅ CHANGE 7: skips silent parts automatically
#         )
#         text = " ".join([s.text for s in segments])
#         print(f"  Done: {text[:80]}...")
#         return text

#     else:
#         segments, _ = model.transcribe(
#             chunk_path,
#             task=task,
#             language=source_lang,
#             beam_size=1,
#             vad_filter=True,
#         )
#         return " ".join([s.text for s in segments])


# def transcribe_all(chunks: list, translate: bool = False, source_lang: str = None) -> str:
#     """
#     Transcribe all chunks.
    
#     Args:
#         chunks:      List of audio chunk file paths
#         translate:   If True, output will always be in English
#         source_lang: Force a language code ("hi", "en", etc.) or None to auto-detect
#     """
#     full_transcript = ""

#     for i, chunk in enumerate(chunks):
#         print(f"\nTranscribing chunk {i + 1}/{len(chunks)}: {chunk}")
#         text = transcribe_chunk(chunk, translate=translate, source_lang=source_lang)
#         full_transcript += text.strip() + " "

#     print("\nTranscription completed.")
#     return full_transcript.strip()

from faster_whisper import WhisperModel

# Load the model once when the file is imported
# "small" = small model (fast, good enough for Hindi/English)
# "int8" = compressed version (uses less RAM, faster on CPU)
# cpu_threads=2 = don't overload your RAM (yours is at 92%)
model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)


def detect_language(audio_path: str) -> str:
    """
    Listen to the audio and detect what language it is.
    Returns "hi" for Hindi, "en" for English, etc.
    """
    _, info = model.transcribe(audio_path, beam_size=1)
    print(f"  Detected language: {info.language} (confidence: {info.language_probability:.2f})")
    return info.language


def transcribe_all(chunks: list, translate: bool = True) -> str:
    """
    Takes a list of audio chunks and converts speech to text.

    chunks    = list of audio file paths (e.g. ["chunk_0.wav", "chunk_1.wav"])
    translate = True  → always give output in English (even if audio is Hindi/Hinglish)
                False → give output in original language
    
    NOTE: language is auto detected per chunk
          so Hinglish videos are handled automatically
    """

    full_text = ""  # we will keep adding text here as each chunk is done

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}/{len(chunks)}")

        # detect language for EACH chunk automatically
        # this handles Hinglish — some chunks may be "hi", some "en"
        lang = detect_language(chunk)

        # Hinglish handling:
        # if confidence is low it's probably Hinglish (mixed Hindi+English)
        # in that case just let whisper figure it out without forcing a language
        _, info = model.transcribe(chunk, beam_size=1)
        if info.language_probability < 0.8:
            print(f"  Low confidence — likely Hinglish, auto-detecting...")
            lang = None   # None = whisper decides on its own per segment

        # task = "translate" means output will always be in English
        # task = "transcribe" means output stays in original language
        if lang == "en":
            task = "transcribe"
        else:
            task = "translate"

        print(f"  Language: {lang or 'auto'} | Task: {task}")

        # transcribe the chunk
        segments, _ = model.transcribe(
            chunk,
            language=lang,   # None for Hinglish = auto per segment
            task=task,
            beam_size=1,     # beam_size=1 = fastest
            vad_filter=True, # skip silent parts automatically
        )

        # print each sentence live as it's transcribed
        for s in segments:
            full_text += s.text.strip() + " "

    print("\nTranscription complete.")

    print("\n" + "=" * 60)
    print("Transcript:\n")
    print(full_text.strip())
    print("=" * 60)

    return full_text.strip()