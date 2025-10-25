import sounddevice as sd


class AudioStream:
    def __init__(self,sample_rate=44100,  chunk_size=1024, callback=None):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.callback = callback

    def start(self):
        sd.InputStream(channels=1, samplerate=self.sample_rate,
                       blocksize=self.chunk_size,
                       callback=self._audio_callback).start()

    def _audio_callback(self, indata, frames, time, status):
        if self.callback:
            self.callback(indata[:, 0])
