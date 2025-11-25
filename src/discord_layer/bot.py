import discord
import os
from dotenv import load_dotenv

# Importiamo le nostre funzioni custom
from src.discord_layer.webhook_mgr import send_as_character
# from src.game_logic.flow import UndercoverFlow (Decommenta quando hai il flow pronto)

load_dotenv()

# --- CONFIGURAZIONE ---
GAME_CHANNEL_ID = int(os.getenv("DISCORD_GAME_CHANNEL_ID"))
DEBUG_CHANNEL_ID = int(os.getenv("DISCORD_DEBUG_CHANNEL_ID"))
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Setup Client
intents = discord.Intents.default()
intents.message_content = True # Fondamentale per leggere la chat
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot avviato come {client.user}')
    print(f'   Ascolto sul canale ID: {GAME_CHANNEL_ID}')
    print(f'   Debug sul canale ID:   {DEBUG_CHANNEL_ID}')

@client.event
async def on_message(message):
    # 1. Ignora i messaggi del bot stesso o dei webhook
    if message.author.bot or message.webhook_id:
        return

    # 2. Ignora i messaggi che non sono nel canale di gioco
    if message.channel.id != GAME_CHANNEL_ID:
        return

    print(f"📩 Messaggio ricevuto da {message.author}: {message.content}")

    # --- QUI INIZIA LA LOGICA AI ---
    
    # A. Eseguiamo l'analisi del Giudice (Simulazione)
    # In futuro: judge_result = flow.execute_judge(message.content)
    suspicion_score = 45 # Valore finto per test
    suspicion_reason = "Domanda tecnica sul furgone, ma accettabile."

    # B. Invio Report al Canale Debug (Solo per te)
    debug_channel = client.get_channel(DEBUG_CHANNEL_ID)
    if debug_channel:
        color = discord.Color.green() if suspicion_score < 60 else discord.Color.red()
        embed = discord.Embed(title="🕵️ Analisi 'L'Ombra'", color=color)
        embed.add_field(name="Input Utente", value=message.content, inline=False)
        embed.add_field(name="Sospetto", value=f"{suspicion_score}/100", inline=True)
        embed.add_field(name="Motivo", value=suspicion_reason, inline=False)
        await debug_channel.send(embed=embed)
    
    # C. Gestione Risposta Pubblica (Game Over o Risposta Criminale)
    if suspicion_score > 80:
        # GAME OVER
        await send_as_character(WEBHOOK_URL, "boss", "Hai fatto troppe domande. Sei fuori! 🔫")
    else:
        # IL GIOCO CONTINUA
        # In futuro: response_data = flow.execute_crew(message.content)
        
        # Simuliamo che risponda Dante (il nuovo agente armato)
        fake_agent_response = "Il furgone regge, ma vedi di non farci saltare sulle buche o il C4 esplode."
        agent_speaking = "bomber-thief" 

        # Usiamo il Webhook per rispondere nel canale pubblico
        await send_as_character(WEBHOOK_URL, agent_speaking, fake_agent_response)