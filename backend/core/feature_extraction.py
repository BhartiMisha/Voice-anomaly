import io
import numpy as np
import librosa

def extract_behavior_features(audio_bytes: bytes):
    """
    Extract behavioral voice features like pitch, tempo, MFCC using librosa.
    Returns dict: { pitch, tempo, mfcc }
    """
    try:
        audio_stream = io.BytesIO(audio_bytes)
        y, sr = librosa.load(audio_stream, sr=None)

        # Pitch estimation (YIN algorithm)
        pitches, _ = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[pitches > 0]
        pitch_mean = float(np.mean(pitch_values)) if pitch_values.size > 0 else 0.0

        # Tempo (beats per minute)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # MFCC
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = mfcc.mean(axis=1).tolist()  # Average across time

        return {
            "pitch": round(pitch_mean, 2),
            "tempo": round(float(tempo), 2),
            "mfcc": mfcc_mean
        }
    except Exception as e:
        print(f"Error extracting behavior features: {e}")
        return {"pitch": 0.0, "tempo": 0.0, "mfcc": []}
