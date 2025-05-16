from google import genai
from google import genai
from google.genai.types import HttpOptions, Part
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gemini/credentials.json'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'pcloud2025'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'europe-west8'
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'

client = genai.Client(http_options=HttpOptions(api_version="v1"))

prompt = "Cosa è rappresentato nell'immagine?"

client = genai.Client(http_options=HttpOptions(api_version="v1"))
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=[
        "Descrivi l'immagine",
        Part.from_uri(
            file_uri="gs://upload_pcloud2025/cyber.jpg",
            mime_type="image/jpeg",
        ),
    ],
)
print(response.text)