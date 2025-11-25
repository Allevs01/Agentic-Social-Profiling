from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_gemini_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite", # Sostituisci con il nome modello esatto
        verbose=True,
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )