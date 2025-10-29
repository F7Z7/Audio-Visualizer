import soundfile as sf
import numpy as np
import time

class AudioFileInput:
    def __init__(self, audio_file_path,chunk_size=1024, callback=None):
        self.audio_file_path = audio_file_path
        self.chunk_size = chunk_size
        self.callback = callback
        self.stream_running=False


    def start(self):
        data,samplerate = sf.read(self.audio_file_path,dtype='float32')
        self.samplerate = samplerate
        self.stream_running=True


        num_chunks=len(self.data)//self.chunk_size

        for i in range(num_chunks):
            if not self.stream_running:
                break
            chunk = data[i * self.chunk_size: (i + 1) * self.chunk_size]
            if self.callback:
                self.callback(chunk)
            time.sleep(self.chunk_size / self.sample_rate)

    def stop(self):
        self.stream_running=False