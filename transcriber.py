from google.cloud import speech
from audio_recorder import AudioRecorder 
from chatbot import ChatBot 
from textoAVoz import TextToSpeech
from test_openai import claseOpenAI 
from reproductor import Reproductor
class AudioTranscriber:
    def __init__(self):
        self.client = speech.SpeechClient()
    def transcribe_audio(self, audio_file_path):
        client = self.client
        with open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=48000,
            language_code="es-ES",
        )
        response = client.recognize(config=config, audio=audio)
        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")
        return response.results[0].alternatives[0].transcript
    
def grabar_audio():
    while True:
        audio_recorder = AudioRecorder(silenceDuration=4, record_seconds=30, save_path="audiosMp3/audio.mp3")
        audio = audio_recorder.record_audio()
        transcriber = AudioTranscriber()
        transcripcion = transcriber.transcribe_audio(audio_file_path=audio)
        respuesta = chatGPTIA.obtener_respuesta(transcripcion)
        recorder.synthesize_speech(respuesta, output_file_path="audiosMp3/output.mp3")
        speacker.reproducir_audio("audiosMp3/output.mp3")
        if False:
            break
if __name__ == "__main__":
    transcriber = AudioTranscriber()
    #chatBot = ChatBot()
    #respuesta = chatBot.chat_loop(transcripcion)
    api_key = "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" 
    chatGPTIA = claseOpenAI(api_key)
    recorder = TextToSpeech() 
    speacker = Reproductor()
    nombre = "Anthonny Montero"
    script_inicial = f'Buenos días tengo el gusto con {nombre}, le saludamos de Manufacturera Ecuatoriana "Primero Ecuador"'
    recorder.synthesize_speech(script_inicial, output_file_path="saludoInicial.mp3")
    speacker.reproducir_audio("saludoInicial.mp3")
    grabar_audio(); 

