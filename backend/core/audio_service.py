import sounddevice as sd
import numpy as np
from backend.core.audio_analysis import AudioAnalyzer

class AudioService:
    def __init__(self, sample_rate=16000, chunk_duration=1.0):
        self.sample_rate = sample_rate
        self.chunk_size = int(sample_rate * chunk_duration)
        self.analyzer = AudioAnalyzer(sample_rate=self.sample_rate)
        self.is_running = False
        self.stream = None

    def start(self, callback=None):
        self.is_running = True

        def audio_callback(indata, frames, time_info, status):
            if not self.is_running:
                return
            audio_data = indata[:, 0].copy()
            metrics = self.analyzer.analyze_audio_chunk(audio_data)
            if callback and metrics:
                callback(metrics)

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype='float32',
            blocksize=self.chunk_size,
            callback=audio_callback
        )
        self.stream.start()

    def stop(self):
        self.is_running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None