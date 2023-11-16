from openai import OpenAI
from pathlib import Path

OPENAI_KEY = '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'
ORGANIZATION_ID = 'org-nikZJpRdZSBtqUGYfMXbvqRL'

client = OpenAI(
    organization=ORGANIZATION_ID,
    api_key=OPENAI_KEY,
)
# models = client.models.list()

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1-hd-1106",
  voice="alloy",
  input="Today is a wonderful day to build something people love!",
    speed=0.9,
)

response.stream_to_file(speech_file_path)
