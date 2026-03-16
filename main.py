import os
import base64
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = genai.Client(api_key=os.getenv("AIzaSyD9Z958n2KyjjMo9DZpP3toGmaAsUhJHuI"))

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_prompt = data.get("prompt")
    image_data = data.get("image") # Base64 string if any

    # AXON's New Personality Logic
    instruction = """
    You are AXON, a high-level intellectual AI. 
    Follow this STRICT response structure for every query:
    1. RECOGNITION: Briefly acknowledge the user's situation or question (Max 30 words).
    2. CORE ANALYSIS: Provide a detailed, logical solution or explanation.
    3. ACTION/SUMMARY: A short, 1-line 'Real-life' actionable advice or conclusion.
    
    Tone: Professional, bold, and honest (No 'chaaplusi'). Use the language the user speaks.
    """

    contents = []
    if image_data:
        # Handle Image/File
        contents.append(types.Part.from_bytes(
            data=base64.b64decode(image_data),
            mime_type="image/jpeg"
        ))
    
    contents.append(user_prompt)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config={'system_instruction': instruction}
        )
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}
        from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# CORS allow karna zaroori hai taaki tumhara HTML baat kar sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini Setup
# Render ke Environment Variables mein 'GEMINI_API_KEY' naam se apni key daalna
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "AXON Engine is Live"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = model.generate_content(request.prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
