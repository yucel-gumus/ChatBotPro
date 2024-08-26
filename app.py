import os
import gradio as gr
from google import generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class ChatSession:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])

    def ask_question(self, question):
        response = self.chat.send_message(question)
        return response.text

def chat_with_gemini(input_text, history):
    chat_session = ChatSession()
    response = chat_session.ask_question(input_text)
    history.append((input_text, response))
    return history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(label="Sohbet Geçmişi")
    msg = gr.Textbox(label="Mesajınız", placeholder="Sorunuzu buraya yazın...")
    send = gr.Button("Gönder")
    clear = gr.Button("Temizle")

    def respond(message, chat_history):
        chat_history = chat_with_gemini(message, chat_history)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    send.click(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch()