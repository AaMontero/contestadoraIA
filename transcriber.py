from google.cloud import speech
from audio_recorder import AudioRecorder 
from chatbot import ChatBot 
from textoAVoz import TextToSpeech
class AudioTranscriber:
    def __init__(self, audio_file_path):
        self.audio_file_path = audio_file_path
    def transcribe_audio(self):
        client = speech.SpeechClient()
        with open(self.audio_file_path, "rb") as audio_file:
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
if __name__ == "__main__":
    audio_recorder = AudioRecorder()
    audio_recorder.record_audio()
    transcriber = AudioTranscriber(audio_file_path=audio_recorder.WAVE_OUTPUT_FILENAME)
    transcripcion = transcriber.transcribe_audio()
    chatBot = ChatBot()
    respuesta = chatBot.chat_loop(transcripcion)
    speaker = TextToSpeech(respuesta, output_file_path="audiosMp3/output.mp3") 
    speaker.synthesize_speech()


