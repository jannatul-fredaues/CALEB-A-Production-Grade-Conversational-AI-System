from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "Hello, reply with one sentence."}
    ]
)

print(response.choices[0].message.content)
