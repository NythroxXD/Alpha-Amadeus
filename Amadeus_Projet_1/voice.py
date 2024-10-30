from elevenlabs import play, ElevenLabs
import vlc
import os
from dotenv import load_dotenv
import speech_recognition as sr
import numpy as np
import time

load_dotenv()  # Charger les variables d'environnement depuis le fichier .env

client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))

def text_to_speech(text):
    # Génère l'audio à partir du texte fourni
    audio = client.generate(
        text=text,
        voice="x10MLxaAmShMYt7vs7pl",
        model="eleven_multilingual_v2"
    )
    audio_bytes = b"".join(audio)

    with open("output_audio.mp3", "wb") as f:
        f.write(audio_bytes)

    instance = vlc.Instance()

    # Player 1
    player1 = instance.media_player_new()
    media1 = instance.media_new("output_audio.mp3")
    player1.set_media(media1)
    player1.audio_output_device_set(None, "{0.0.0.00000000}.{78e2b4bd-7754-46af-aada-36282b8f6d94}")
    player1.audio_set_volume(100)

    # Player 2
    player2 = instance.media_player_new()
    media2 = instance.media_new("output_audio.mp3")
    player2.set_media(media2)
    player2.audio_output_device_set(None, "{0.0.0.00000000}.{90724f32-281c-4c65-a88e-6a99d3cd5f81}")
    player2.audio_set_volume(100)

    # Attacher les événements pour vérifier les erreurs
    player1.event_manager().event_attach(vlc.EventType.MediaPlayerEncounteredError, lambda e: print("Erreur avec player1"))
    player2.event_manager().event_attach(vlc.EventType.MediaPlayerEncounteredError, lambda e: print("Erreur avec player2"))

    # Lecture
    player1.play()
    time.sleep(0.5)
    player2.play()

    # Attendre que les players finissent de jouer
    while player1.is_playing() or player2.is_playing():
        time.sleep(0.1)


def speech_to_text(is_recording_callback):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustement du bruit ambiant, veuillez patienter...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Parlez maintenant...")

        while is_recording_callback():
            try:
                # Écouter l'audio sans limite de temps
                audio = recognizer.listen(source)
                print("Traitement en cours...")
                text = recognizer.recognize_google(audio, language="fr-FR")
                print(f"Vous avez dit : {text}")
                return text

            except sr.UnknownValueError:
                print("Je n'ai pas compris, veuillez réessayer.")
                # Continuer la boucle pour que l'utilisateur réessaye
                continue

            except sr.RequestError as e:
                print(f"Erreur avec le service de reconnaissance vocale : {e}")
                return None

            except Exception as e:
                print(f"Une erreur inattendue s'est produite : {e}")
                return None

        # Retourner None si l'enregistrement est arrêté
        print("Enregistrement arrêté.")
        return None