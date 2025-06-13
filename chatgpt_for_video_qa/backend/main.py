# # main.py
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# import requests
# # If you have GPT-Chat endpoint, or you can use OpenAI API here:

# # Mock GPT-Chat
# def gpt_chat(prompt: str) -> str:
#     return f"Mock answer for: {prompt}"


# # Mock transcript retrieval
# def get_youtube_transcript(video_id: str) -> str:
#     return f"Transcript for video {video_id}. (Mock)"

# app = FastAPI()

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# class ChatRequest(BaseModel):
#     videoId: str
#     question: str


# @app.post('/chat')
# def chat(data: ChatRequest):
#     videoId = data.videoId
#     question = data.question

#     transcript = get_youtube_transcript(videoId)
#     prompt = f"""This is the transcript of a YouTube video:\n{transcript}\nQuestion: {question}\nPlease respond briefly and accurately."""    

#     answer = gpt_chat(prompt)
#     return {"answer": answer}

