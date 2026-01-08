from flask import Flask, request, jsonify
from flask_cors import CORS
import google.genai as genai
from dotenv import load_dotenv
from google.genai import Client
import os

# ---------------------------
# Flask Setup
# ---------------------------
app = Flask(__name__)
CORS(app)  # allows frontend to send requests

# ---------------------------
# Gemini API Key
# ---------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


# ---------------------------
# Home route (test server)
# ---------------------------
@app.route("/")
def index():
    return "Hello, Flask is working 🎉"

# ---------------------------
# Chat endpoint
# ---------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"reply": "Please type a message."})

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=user_message
        )

        bot_reply = response.text

    except Exception as e:
        bot_reply = "Sorry, I am having trouble responding right now."
        print("Gemini API Error:", e)  # Print error in terminal for debugging

    return jsonify({"reply": bot_reply})

# ---------------------------
# Run Flask server
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
