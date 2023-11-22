from pydub import AudioSegment
from pydub.playback import play

def reproducir_audio(nombre_archivo):
    # Cargar el archivo de audio
    audio = AudioSegment.from_file(nombre_archivo)

    # Reproducir el audio
    play(audio)

# Ejemplo de uso
nombre_archivo = 'output.mp3'  # Reemplaza con el nombre de tu archivo de audio
reproducir_audio(nombre_archivo)