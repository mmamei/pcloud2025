from google import genai
from google import genai
from google.genai.types import HttpOptions
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gemini/credentials.json'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'pcloud2025'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'europe-west8'
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'

prompt = input("Enter your prompt: ")

client = genai.Client(http_options=HttpOptions(api_version="v1"))
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt,
)
print(response.text)