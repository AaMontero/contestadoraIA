from pydub import AudioSegment
from pydub.playback import play
class Reproductor: 
    def reproducir_audio(self, nombre_archivo):
        # Cargar el archivo de audio
        audio = AudioSegment.from_file(nombre_archivo)
        # Reproducir el audio
        play(audio)
