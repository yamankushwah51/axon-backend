import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

@app.get("/")
def status():
    return {"message": "AXON AI Backend is Active", "version": "1.0"}

@app.post("/chat")
async def chat(prompt: str, user_gender: str = "male", is_serious: bool = False):
    gender_tone = "Brother/Dost" if user_gender == "male" else "Sister/Friend"
    
    instruction = f"""
    You are AXON, a smart Indian AI {gender_tone}. 
    - Respond in natural Hinglish.
    - Be firm and honest (No Chaaplusi). If you have an opinion, stick to it.
    - Context Detection: If 'is_serious' is true, be deeply logical and limit to 70 words.
    - If user is joking, be funny and chill.
    - Never apologize unless you made a factual error.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={'system_instruction': instruction}
        )
        return {"response": response.text}
    except Exception as e:
        return {"error": "Server issue, please try again!"}
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_prompt = data.get("prompt")
    # Language detection aur response logic ab Gemini natively handle karega
    
    instruction = """
    You are AXON, a multi-lingual AI. 
    - Respond in the language used by the user (Hindi, English, Tamil, Japanese, Hinglish, etc.).
    - Keep the AXON personality: Honest, bold, and logical.
    - No 'chaaplusi'. If the user is wrong, tell them politely but firmly.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_prompt,
            config={'system_instruction': instruction}
        )
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}
