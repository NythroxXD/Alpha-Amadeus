# Contrôle des mouvements de la bouche
import pyvts
import asyncio, threading, os, time, base64, random
from colorama import *
from gpt import get_chat_response
from elevenlabs import text_to_speech as speak

# Initialisation de la connexion VTube Studio
VTS = pyvts.vts(
    plugin_info={
        "plugin_name": "Amadeus-vtuber",
        "developer": "Nythrox",
        "authentication_token_path": "./token.txt",
    },
    vts_api_info={
        "version": "1.0",
        "name": "VTubeStudioPublicAPI",
        "port": int(os.environ.get("VTUBE_STUDIO_API_PORT", 8001))
    }
)

# Le paramètre par défaut pour le mouvement de la bouche
VOICE_PARAMETER = "MouthOpen"

EVENT_LOOP = None
VOICE_LEVEL = 0

async def connect_vts():
    global VTS
    tries = 0
    while tries < 10:
        try:
            if VTS.get_connection_status() == 0:
                await VTS.connect()
                print("Connexion à VTube Studio réussie!")
            if VTS.get_authentic_status() < 2:
                print(f"Demande d'authentification envoyée à VTube Studio, veuillez{Fore.GREEN}{Style.BRIGHT} cliquer sur autoriser{Fore.RESET}{Style.RESET_ALL}.")
                await VTS.request_authenticate_token()
                await VTS.request_authenticate()
                await VTS.write_token()
            if VTS.get_authentic_status() == 2:
                print("Authentification réussie!")
                break
        except Exception as e:
            tries += 1
            print(f"> Tentative de connexion à VTube Studio {Fore.RED}tentative {tries}{Fore.RESET}")
            print(f"Erreur: {e}")
            time.sleep(7 if tries > 7 else tries)

async def start():
    global VTS, VOICE_LEVEL
    await connect_vts()

    # Boucle pour ajuster le niveau de mouvement de la bouche en fonction de la voix
    current_voice_level = 0
    while True:
        try:
            if VOICE_LEVEL != current_voice_level:
                if VTS.get_connection_status() == 1 and VTS.get_authentic_status() == 2:
                    await VTS.request(
                        VTS.vts_request.requestSetParameterValue(parameter=VOICE_PARAMETER, value=VOICE_LEVEL)
                    )
                    current_voice_level = VOICE_LEVEL
                else:
                    print("Perte de connexion avec VTube Studio, tentative de reconnexion...")
                    await connect_vts()
        except Exception as e:
            print(f"Erreur lors de la mise à jour du mouvement de la bouche: {e}")
        await asyncio.sleep(1/60)  # 60 fps pour une réponse fluide

def set_audio_level(level):
    # Ajuste le niveau de la bouche en fonction de la réponse générée par l'IA
    global VOICE_PARAMETER, VOICE_LEVEL
    print(f"Définir le niveau audio à: {level}")  # Log pour vérifier le niveau
    VOICE_LEVEL = level

from concurrent.futures import ThreadPoolExecutor

def start_real():
    global EVENT_LOOP  
    EVENT_LOOP = asyncio.new_event_loop()
    EVENT_LOOP.run_until_complete(start())

def run_async():  
    t = threading.Thread(target=start_real)
    t.daemon = True
    t.start()

# Exemple d'utilisation avec la réponse de l'IA
def handle_chat_response(user_input):
    print(f"Génération de la réponse pour: {user_input}")  # Log pour vérifier la réponse de l'utilisateur
    response = get_chat_response(user_input)
    # Début du mouvement de la bouche
    for i in range(10):
        set_audio_level(random.uniform(0.5, 1.0))  # Variation pour simuler la parole
        time.sleep(0.1)
    speak(response)
    # Fin du mouvement de la bouche
    set_audio_level(0.0)

# Lancer la connexion avec VTube Studio
run_async()
