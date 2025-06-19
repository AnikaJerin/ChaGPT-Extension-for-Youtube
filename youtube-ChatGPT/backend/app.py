# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable
import tiktoken

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key="gdy83838")  # It's a demo. Replace with  actual key

# Set token limits
MAX_CONTEXT_TOKENS = 3500  # gpt-3.5-turbo supports max 4096 tokens
MAX_SUMMARY_TOKENS = 500   # tokens reserved for summary

# Use OpenAI tokenizer
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def num_tokens_from_string(string):
    return len(encoding.encode(string))


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    video_id = data.get("videoId")
    question = data.get("question")

    if not video_id or not question:
        return jsonify({"error": "Missing videoId or question"}), 400

    # Try fetching transcript
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item['text'] for item in transcript_data])
    except (TranscriptsDisabled, VideoUnavailable):
        return jsonify({"error": "Unable to fetch transcript"}), 500

    # Count tokens in transcript
    transcript_tokens = num_tokens_from_string(transcript)

    # If too long, summarize it first
    if transcript_tokens > MAX_CONTEXT_TOKENS:
        try:
            summary_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Summarize the following transcript. The summary should help answer questions about the content."},
                    {"role": "user", "content": transcript[:8000]}  # Truncate to avoid overflow
                ],
                max_tokens=MAX_SUMMARY_TOKENS,
                temperature=0.5
            )
            transcript = summary_response.choices[0].message.content.strip()
        except Exception as e:
            return jsonify({"error": f"Failed to summarize transcript: {str(e)}"}), 500

    # Prepare final prompt
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




