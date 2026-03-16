import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


API_KEY = os.environ.get("AIzaSyD9Z958n2KyjjMo9DZpP3toGmaAsUhJHuI")
genai.configure(api_key=API_KEY)

SYSTEM_INSTRUCTION = """
You are AXON, a high-level intellectual AI. 
Follow this STRICT response structure:
1. RECOGNITION: Briefly acknowledge the user (Max 30 words).
2. CORE ANALYSIS: Provide a detailed, logical solution.
3. ACTION: A short, 1-line actionable advice.

Tone: Professional, bold, and honest. Use the language the user speaks (Hinglish/Hindi/English).
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "AXON Engine is Live", "message": "System Ready"}

@app.post("/chat")
async def chat(request: ChatRequest):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API Key missing on server!")
    
    try:
        response = model.generate_content(request.prompt)
        return {"response": response.text}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
