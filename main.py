from flask import Flask, request, jsonify
from flask_cors import CORS
import pyttsx3
import datetime
import webbrowser
import os

app = Flask(__name__)
CORS(app)

# ================= VOICE OUTPUT =================
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ================= ASSISTANT STATE =================
assistant_awake = False
conversation_memory = []

# ================= COMMAND HANDLER =================
def handle_command(text):
    global assistant_awake

    # TIME
    if "time" in text:
        return f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"

    # DATE
    if "date" in text:
        return f"Today is {datetime.datetime.now().strftime('%A, %d %B %Y')}"

    # OPEN WEBSITES
    if "open google" in text:
        webbrowser.open("https://google.com")
        return "Opening Google"

    if "open youtube" in text:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    # SYSTEM COMMANDS
    if "shutdown" in text:
        return "Shutdown command received. Permission required."

    if "restart" in text:
        return "Restart command received. Permission required."

    # MEMORY
    if "what did i say" in text:
        if conversation_memory:
            return "You said: " + ", ".join(conversation_memory[-3:])
        return "You haven't said anything yet"

    # FALLBACK (AI READY)
    return "I heard you, master, but I need more training for that."

# ================= API ENDPOINT =================
@app.route("/command", methods=["POST"])
def command():
    global assistant_awake

    data = request.json
    text = data.get("text", "").lower().strip()

    print("USER:", text)

    if not text:
        return jsonify({"reply": "No input received", "awake": assistant_awake})

    conversation_memory.append(text)

    # WAKE WORD
    if "candy" in text and not assistant_awake:
        assistant_awake = True
        reply = "Hi master"
        speak(reply)
        return jsonify({"reply": reply, "awake": assistant_awake})

    # IGNORE COMMANDS IF SLEEPING
    if not assistant_awake:
        return jsonify({
            "reply": "Say 'Candy' to wake me up",
            "awake": assistant_awake
        })

    # HANDLE COMMAND
    reply = handle_command(text)
    speak(reply)

    # GO BACK TO SLEEP
    assistant_awake = False

    return jsonify({
        "reply": reply,
        "awake": assistant_awake
    })

# ================= HOME (OPTIONAL) =================
@app.route("/")
def home():
    return "Candy backend is running"

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
