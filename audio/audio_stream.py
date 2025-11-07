import sounddevice as sd


class AudioStream:
    def __init__(self,sample_rate=44100,  chunk_size=1024, callback=None,use_system_audio=True):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.callback = callback
        self.stream=None
        self.use_system_audio=use_system_audio

    def start(self):

        device=None
        if self.use_system_audio:
            devices=sd.query_devices()
            for i, d in enumerate(devices):
                if 'loopback' in d['name'].lower() or 'stereo mix' in d['name'].lower():
                    device = i
                    print(f"[INFO] Using loopback device: {d['name']}")
                    break

        self.stream=sd.InputStream(
            device=device,
            channels=2,
            samplerate=self.sample_rate,
            blocksize=self.chunk_size,
            callback=self._audio_callback)
        self.stream.start()


    def _audio_callback(self, indata, frames, time, status):
        if self.callback:
            self.callback(indata[:, 0])
            mono = indata.mean(axis=1)
            self.callback(mono)

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream=None