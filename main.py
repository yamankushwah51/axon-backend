import os
import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai

app = FastAPI()

# Frontend connection ke liye CORS bypass
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


API_KEY = os.environ.get("AIzaSyD9Z958n2KyjjMo9DZpP3toGmaAsUhJHuI")
genai.configure(api_key=API_KEY)


model = genai.GenerativeModel('gemini-2.0-flash')

class ChatRequest(BaseModel):
    prompt: str
    image_data: Optional[str] = None  # Frontend se image base64 mein aayegi

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        
        instruction = "You are AXON, a high-level intellectual AI. Keep your tone bold and tech-savvy."
        content = [instruction, request.prompt]
        
        
        if request.image_data:
            try:
                img_bytes = base64.b64decode(request.image_data)
                content.append({"mime_type": "image/jpeg", "data": img_bytes})
            except:
                pass # Agar image format galat hai toh skip karo
        
        response = model.generate_content(content)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "AXON Engine is running on Light Speed"}
    
