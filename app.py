from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Configure Gemini API
api_key = os.getenv("GEMINI_KEY")

if not api_key:
    raise ValueError("GEMINI_KEY environment variable not set")

genai.configure(api_key=api_key)

# Correct model name
model = genai.GenerativeModel("gemini-1.5-flash-latest")


@app.route("/")
def home():
    return "SmartCrack AI Backend Running"


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"reply": "Please send a message."})

        user_message = data["message"]

        prompt = f"""
You are a helpful AI tutor for students.

Student question:
{user_message}

Answer clearly.
"""

        response = model.generate_content(prompt)

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "reply": "AI server error. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)