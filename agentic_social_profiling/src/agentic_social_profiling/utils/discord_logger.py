import os
import requests
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()


# AGENT_AVATARS = {
#     "Boss": "https://url_immagine_ricercatore.png",
#     "Writer": "https://url_immagine_writer.png"
# }

def _send_webhook(username, content):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ Warning: Nessun Webhook URL trovato nel file .env")
        return

    data = {
        "username": username,
        "content": content
        # "avatar_url": avatar_url
    }
    try:
        requests.post(webhook_url, json=data)
    except Exception as e:
        print(f"Errore Discord: {e}")

def task_callback(output):
    """
    Questa è l'unica funzione che importerai nel main.
    """
    # Logica di formattazione
    agent_role = output.agent
    content = output.raw
    
    # Tronca se troppo lungo
    if len(content) > 1900:
        content = content[:1900] + "...\n*(Vedi output completo in console)*"
        
    # Recupera avatar
    # avatar = AGENT_AVATARS.get(agent_role)
    
    # Invia
    _send_webhook(agent_role, content)