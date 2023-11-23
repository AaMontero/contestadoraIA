import pyaudio
import wave
import audioop

class AudioRecorder:
    def __init__(self, silenceDuration, record_seconds, save_path):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 48000
        self.RECORD_SECONDS = record_seconds
        self.WAVE_OUTPUT_FILENAME = save_path
        self.ENERGY_THRESHOLD = 3500
        self.SILENCE_DURATION = silenceDuration

        self.p = pyaudio.PyAudio()

    def record_audio(self):
        stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        print("Grabando...")

        frames = []
        silence_counter = 0

        while True:
            data = stream.read(self.CHUNK)
            frames.append(data)
            energy = audioop.rms(data, 2)
            print(self.WAVE_OUTPUT_FILENAME +" "+ str(silence_counter))
            if energy < self.ENERGY_THRESHOLD:
                silence_counter += 1
            else:
                silence_counter -= 0.5

            if silence_counter >= int(self.RATE / self.CHUNK * self.SILENCE_DURATION):
                break

        print("Terminado de grabar")

        stream.stop_stream()
        stream.close()
        self.p.terminate()
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"Grabación guardada en '{self.WAVE_OUTPUT_FILENAME}'")
        return(self.WAVE_OUTPUT_FILENAME)
