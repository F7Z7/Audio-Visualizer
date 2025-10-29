import soundfile as sf
import sounddevice as sd
import time
import numpy as np

class AudioFileInput:
    def __init__(self, audio_file_path, chunk_size=1024, callback=None):
        self.audio_file_path = audio_file_path
        self.chunk_size = chunk_size
        self.callback = callback
        self.stream_running = False

    def start(self):
        data, samplerate = sf.read(self.audio_file_path, dtype='float32')
        self.samplerate = samplerate
        self.stream_running = True

        num_chunks = len(data) // self.chunk_size


        with sd.OutputStream(samplerate=self.samplerate, channels=data.shape[1] if data.ndim > 1 else 1):
            for i in range(num_chunks):
                if not self.stream_running:
                    break

                chunk = data[i * self.chunk_size: (i + 1) * self.chunk_size]

                sd.wait()
                sd.play(chunk, self.samplerate, blocking=False)

                if self.callback:
                    if data.ndim > 1:
                        self.callback(np.mean(chunk, axis=1))
                    else:
                        self.callback(chunk)

                time.sleep(self.chunk_size / self.samplerate)

    def stop(self):
        self.stream_running = False
        sd.stop()
