
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("API_KEY"))

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Hello, reply with one sentence."
)

print(response.output_text)
