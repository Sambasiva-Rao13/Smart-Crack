from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return jsonify({"reply": response.text})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
