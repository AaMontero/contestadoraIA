from google.cloud import texttospeech

class TextToSpeech:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, text, output_file_path="audiosMp3/output.mp3"):
        # Instantiates a client
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code ("es-US") and the ssml
        # voice gender ("male")
        voice = texttospeech.VoiceSelectionParams(
            language_code="es-US",
            name="es-US-Neural2-B",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(output_file_path, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f'Audio content written to file "{output_file_path}"')


# Ejemplo de uso
if __name__ == "__main__":
    texto_para_sintetizar = '''Hola, buenas tardes!,
        le saluda Diego Noguera coordinador de entregas de la empresa Qory,
        el motivo de mi llamada, era para informarle que ha sido acreedor de una tarjeta gifcard de consumo,
        debido a su excelente perfil de socios activos.'''
    
    tts = TextToSpeech(texto_para_sintetizar)
    tts.synthesize_speech()