from crewai import LLM
import os

def get_gemini_llm():
    return LLM(
        model="gemini/gemini-1.5-flash",
        verbose=True,
        temperature=0.7,
        api_key=os.getenv("GOOGLE_API_KEY")
    )