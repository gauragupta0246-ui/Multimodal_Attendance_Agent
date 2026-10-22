import librosa
import numpy as np
import os

class AudioAnalyzer:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def analyze_audio_chunk(self, audio_data):
        """
        Analyzes raw audio bytes/array:
        1. Noise level (decibels)
        2. Speech vs silence ratio
        3. Sound activity patterns
        Returns engagement metrics
        """
        try:
            # Convert bytes to float32 numpy array if needed
            if isinstance(audio_data, bytes):
                # Assuming 16-bit PCM
                y = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            else:
                y = audio_data

            if len(y) == 0:
                return None

            # 1. Calculate RMS energy & Noise/Volume Level in dB
            rms = librosa.feature.rms(y=y)[0]
            mean_rms = np.mean(rms)
            db = 20 * np.log10(mean_rms + 1e-6)

            # 2. Speech vs Silence Detection
            silence_threshold = 0.01
            voiced_frames = np.sum(rms > silence_threshold)
            speech_ratio = float(voiced_frames / len(rms)) if len(rms) > 0 else 0.0

            # 3. Sound Activity / Engagement indicator
            is_speaking = speech_ratio > 0.3

            return {
                "noise_level_db": round(float(db), 2),
                "speech_ratio": round(speech_ratio, 2),
                "is_speaking": is_speaking,
                "status": "Active" if is_speaking else "Quiet"
            }
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            return None