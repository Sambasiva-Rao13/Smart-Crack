from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Flask app
app = Flask(__name__)
CORS(app)

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

# Health check route (important for Render)
@app.route("/", methods=["GET"])
def home():
    return "AI Backend Running"

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    try:
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
            model="gemini-1.5-flash",
            contents=prompt
        )

        reply = response.text if hasattr(response, "text") else "No response"

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500


# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render compatible
    app.run(host="0.0.0.0", port=port)