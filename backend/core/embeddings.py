import io
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav

# Initialize encoder once
encoder = VoiceEncoder()

def extract_embedding(audio_bytes: bytes):
    """
    Convert raw audio bytes to a voice embedding vector using Resemblyzer.
    """
    try:
        audio_stream = io.BytesIO(audio_bytes)
        wav = preprocess_wav(audio_stream)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()  # Convert to list for MongoDB storage
    except Exception as e:
        print(f"Error extracting embedding: {e}")
        return []
