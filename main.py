import os
from dotenv import load_dotenv

load_dotenv("P:/Caleb/.env")   # absolute path

print("RAW ENV FILE CONTENT:")
with open("P:/Caleb/.env") as f:
    print(f.read())

from dotenv import load_dotenv
load_dotenv(override=True)

from flask import Flask, request, Response
from flask_cors import CORS
from groq import Groq
from mode_router import detect_mode, get_system_prompt
from context import trim_conversation
import os
import json
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

# --------------------
# Groq Client
# --------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --------------------
# Flask App
# --------------------
app = Flask(__name__)
CORS(app)

# In-memory conversation (single-user)
conversation = []

# --------------------
# Streaming LLM
# --------------------
def stream_llm(user_text):
    global conversation

    mode = detect_mode(user_text)

    # Add system prompt once
    if not conversation:
        conversation.append({
            "role": "system",
            "content": get_system_prompt(mode)
        })

    # Add user message
    conversation.append({"role": "user", "content": user_text})
    conversation = trim_conversation(conversation)

    # Groq streaming call
    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=conversation,
        stream=True,
        temperature=0.7,
        max_tokens=500
    )

    full_reply = ""

    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            token = delta.content
            full_reply += token
            yield f"data: {json.dumps({'token': token})}\n\n"

    # Save assistant reply
    conversation.append({"role": "assistant", "content": full_reply})

    # Final event
    yield f"data: {json.dumps({'done': True, 'mode': mode})}\n\n"

print("API KEY =", os.getenv("gsk_oCVdM8rfLd0aadSwW3aAWGdyb3FYlovj5k65i6J0TaqeCP1o9DiIY"))

# --------------------
# Routes
# --------------------
@app.route("/chat-stream", methods=["GET", "POST"])
def chat_stream():
    data = request.get_json()
    user_text = data.get("text", "").strip()

    if not user_text:
        return Response("Empty input", status=400)

    return Response(stream_llm(user_text), mimetype="text/event-stream")


@app.route("/reset", methods=["POST"])
def reset():
    conversation.clear()
    return {"status": "conversation reset"}


# --------------------
# Main
# --------------------
if __name__ == "__main__":
    print("🚀 CALEB backend running at http://127.0.0.1:5000")
    app.run(debug=True, threaded=True)
