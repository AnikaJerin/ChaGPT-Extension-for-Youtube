from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from chatgpt_driver import chat_with_gpt

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Backend is running!"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question")
        transcript = data.get("transcript")

        if not question or not transcript:
            return jsonify({"error": "Missing question or transcript"}), 400

        answer = asyncio.run(chat_with_gpt(question, transcript))
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=False)  # Turn off debug for less console spam
