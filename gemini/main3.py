from google.cloud import texttospeech
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gemini/credentials.json'


# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized

txt = '''L'immagine è una foto in un ambiente urbano con diversi edifici sullo sfondo. Nel mezzo, c'è un uomo, probabilmente sulla cinquantina, vestito con una camicia bianca a maniche lunghe, jeans e una cintura di pelle nera. Sta sorridendo alla telecamera e tiene in mano una giacca grigia.
Alla sua sinistra si vede un'auto dal design futuristico, una Tesla Cybertruck, in tinta argentata. Intorno all'auto e all'uomo ci sono delle barriere nere per tenere lontana la folla.'''

synthesis_input = texttospeech.SynthesisInput(text=txt)

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="it-IT", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')