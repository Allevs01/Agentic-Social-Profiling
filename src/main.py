import os
from dotenv import load_dotenv
from src.discord_layer.bot import client

# Carica variabili d'ambiente
load_dotenv()

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("Token Discord non trovato nel file .env")
    
    print("Avvio del sistema Undercover...")
    client.run(token)