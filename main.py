import os
import google.generativeai as genai
import gradio as gr

# API Key setup
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def chat_function(message, history):
    try:
        instruction = "You are AXON, a high-level intellectual AI developed by Yaman. Be bold and logical."
        response = model.generate_content([instruction, message])
        return response.text
    except Exception as e:
        return f"Error: Make sure GEMINI_API_KEY is set in Settings. ({str(e)})"

# Ek sundar interface bana rahe hain
demo = gr.ChatInterface(
    fn=chat_function,
    title="AXON CORE v2.0",
    description="Developed by Yaman",
    theme="soft"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
