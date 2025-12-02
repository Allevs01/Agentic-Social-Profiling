import os
import sys
from dotenv import load_dotenv

# Questo blocco try/except serve a gestire gli import
# sia che tu lanci il file direttamente, sia come modulo.
try:
    from src.discord_layer.bot import client
except ImportError:
    # Se Python non trova 'src', proviamo ad aggiungere la root al path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.discord_layer.bot import client

def main():
    # 1. Carica le variabili d'ambiente dal file .env
    load_dotenv()

    # 2. Recupera il token
    token = os.getenv("DISCORD_TOKEN")

    # 3. Controlli di sicurezza pre-avvio
    if not token:
        print("\n❌ ERRORE CRITICO: Variabile 'DISCORD_TOKEN' non trovata.")
        print("   -> Assicurati di aver creato il file '.env' nella cartella principale.")
        print("   -> Assicurati che dentro ci sia scritto: DISCORD_TOKEN=il_tuo_token\n")
        return

    # Recupera altre variabili critiche per avvisare se mancano
    api_key = os.getenv("GOOGLE_API_KEY")
    webhook = os.getenv("DISCORD_WEBHOOK_URL")

    if not api_key:
        print("⚠️ ATTENZIONE: 'GOOGLE_API_KEY' mancante. Gemini non funzionerà.")
    
    if not webhook:
        print("⚠️ ATTENZIONE: 'DISCORD_WEBHOOK_URL' mancante. I personaggi non potranno rispondere.")

    print("\n------------------------------------------------")
    print("   🕵️  UNDERCOVER HEIST AI - SYSTEM STARTUP")
    print("------------------------------------------------")
    print("✅ Variabili d'ambiente caricate.")
    print("🚀 Tentativo di connessione a Discord...")

    # 4. Avvia il Bot
    try:
        client.run(token)
    except discord.errors.LoginFailure:
        print("\n❌ ERRORE LOGIN: Il Token di Discord non è valido.")
    except Exception as e:
        print(f"\n❌ ERRORE IMPREVISTO: {e}")

if __name__ == "__main__":
    main()