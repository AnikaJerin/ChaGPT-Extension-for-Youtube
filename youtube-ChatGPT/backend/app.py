# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("bc8035dfb876978d2dc4f0d7f9a87f06"))

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    video_id = data.get("videoId")
    question = data.get("question")

    if not video_id or not question:
        return jsonify({"error": "Missing videoId or question"}), 400

    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item['text'] for item in transcript_data])
    except (TranscriptsDisabled, VideoUnavailable):
        return jsonify({"error": "Unable to fetch transcript"}), 500

    prompt = f"Context:\n{transcript}\n\nQuestion:\n{question}\nAnswer concisely."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5004, debug=True)
