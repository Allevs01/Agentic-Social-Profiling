import discord
from src.game_logic.flow import UndercoverFlow
from src.discord_layer.webhook_mgr import send_as_character

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_message(message):
    if message.author.bot: return

    # Esempio: Se l'utente scrive nella chat, lo consideriamo input per il Flow
    if message.channel.name == "pianificazione-colpo":
        
        # Istanzia il Flow
        game_flow = UndercoverFlow()
        
        # Esegui il flow passando il messaggio dell'utente
        inputs = {"last_message": message.content}
        result_text = game_flow.kickoff(inputs=inputs)
        
        # Ottieni chi deve rispondere dallo stato del flow (es. "Marco")
        character_name = game_flow.state.current_speaker 
        
        # Invia su Discord tramite Webhook
        await send_as_character(message.channel, character_name, result_text)