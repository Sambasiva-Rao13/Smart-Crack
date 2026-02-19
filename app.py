from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.getenv("GEMINI_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"reply": "Please ask something."})

    prompt = f"""
You are a helpful AI learning assistant for students.
Answer clearly and conversationally.

User: {user_message}
"""

    response = model.generate_content(prompt)

    return jsonify({"reply": response.text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
