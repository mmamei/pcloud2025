def main_describe_photo(request):
    from flask import url_for, redirect
    from google.cloud import storage 
    storage_client = storage.Client()
    # check if the post request has the file part
    file = request.files['file']
    bucket = storage_client.bucket('upload_pcloud2025')
    blob = bucket.blob(f'test5.jpg')
    blob.upload_from_string(file.read(), content_type=file.content_type)


    from google import genai
    from google import genai
    from google.genai.types import HttpOptions, Part
    import os
    #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gemini/credentials.json'
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'pcloud2025'
    os.environ['GOOGLE_CLOUD_LOCATION'] = 'europe-west8'
    os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    prompt = "Descrivi l'immagine in italiano"

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=[
            prompt,
            Part.from_uri(
                file_uri="gs://upload_pcloud2025/test5.jpg",
                mime_type="image/jpeg",
            ),
        ],
    )

    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized

    txt = response.text

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
    audio_content = response.audio_content
    from flask import jsonify
    import base64

    encoded_audio = base64.b64encode(audio_content).decode('utf-8')

    return jsonify({'audio_base64': encoded_audio})


    
