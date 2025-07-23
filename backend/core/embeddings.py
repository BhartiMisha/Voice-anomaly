# backend/core/embeddings.py
import librosa
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
import io

encoder = VoiceEncoder()

def extract_embedding(audio_bytes: bytes):
    """
    Extracts voice embeddings using Resemblyzer.
    Converts MP3/WAV bytes into waveform, then preprocesses.
    """
    try:
        # Decode bytes (MP3 or WAV) into waveform
        audio_stream = io.BytesIO(audio_bytes)
        wav, sr = librosa.load(audio_stream, sr=None, mono=True)

        if wav.size == 0:
            print("Empty audio data")
            return []

        # Preprocess for Resemblyzer
        wav = preprocess_wav(wav, source_sr=sr)

        # Generate embedding
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()

    except Exception as e:
        print(f"Error extracting embedding: {e}")
        return []
