import aiohttp
import json
from discord import Webhook

# Carichiamo i personaggi e le loro facce
try:
    with open("config/characters.json", "r") as f:
        CHARACTERS = json.load(f)
except FileNotFoundError:
    print("ATTENZIONE: config/characters.json non trovato. Userò valori default.")
    CHARACTERS = {}

async def send_as_character(webhook_url, agent_key, message_content):
    """
    Invia un messaggio tramite Webhook mascherandosi da personaggio.
    agent_key: 'boss', 'cop', 'bomber-thief', ecc.
    """
    if not webhook_url:
        print("ERRORE: URL Webhook mancante.")
        return

    # Recupera dati personaggio o usa fallback
    char_data = CHARACTERS.get(agent_key, {
        "username": "Sconosciuto",
        "avatar_url": None
    })

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, session=session)
        await webhook.send(
            content=message_content,
            username=char_data['username'],
            avatar_url=char_data['avatar_url']
        )