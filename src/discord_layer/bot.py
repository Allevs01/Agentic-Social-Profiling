import discord
import os
import asyncio
from dotenv import load_dotenv

# Importiamo le nostre funzioni custom
from src.discord_layer.webhook_mgr import send_as_character
from src.game_logic.flow import UndercoverFlow

load_dotenv()

# --- CONFIGURAZIONE ---
GAME_CHANNEL_ID = int(os.getenv("DISCORD_GAME_CHANNEL_ID"))
DEBUG_CHANNEL_ID = int(os.getenv("DISCORD_DEBUG_CHANNEL_ID"))
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Setup Client
intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

# Inizializza il Flow Globale
GLOBAL_GAME_FLOW = UndercoverFlow()

async def game_loop():
    """Ciclo principale della conversazione automatica."""
    await client.wait_until_ready()
    print("🔄 Avvio ciclo di conversazione automatica...")
    
    # Setup iniziale
    # Simuliamo un messaggio iniziale per far partire il Boss
    GLOBAL_GAME_FLOW.state.last_message = "Dobbiamo rivedere il piano per stasera. Nessun errore."
    
    while not client.is_closed():
        try:
            # Eseguiamo il flow (che è sincrono) in un thread separato per non bloccare Discord
            # kickoff() eseguirà i passaggi definiti in flow.py
            final_text = await client.loop.run_in_executor(None, GLOBAL_GAME_FLOW.kickoff)
            
            # Recupera chi ha parlato
            speaker = GLOBAL_GAME_FLOW.state.current_speaker
            
            # Invia su Discord
            await send_as_character(WEBHOOK_URL, speaker, final_text)
            
            # Debug log
            print(f"🗣️ {speaker}: {final_text}")
            
            # Pausa realistica tra i messaggi
            await asyncio.sleep(10)

        except Exception as e:
            print(f"❌ Errore nel game loop: {e}")
            await asyncio.sleep(5) # Attendi prima di riprovare

@client.event
async def on_ready():
    print(f'✅ Bot avviato come {client.user}')
    print(f'   Ascolto sul canale ID: {GAME_CHANNEL_ID}')
    
    # Avvia il loop in background
    client.loop.create_task(game_loop())

@client.event
async def on_message(message):
    # Ignoriamo tutto, il gioco è automatico.
    # Potremmo aggiungere comandi admin qui se necessario.
    pass