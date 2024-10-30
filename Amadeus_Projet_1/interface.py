import customtkinter as ctk
from threading import Thread
from dotenv import load_dotenv
from voice import text_to_speech, speech_to_text
from gpt import get_chat_response

load_dotenv()

class ChatFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.isRecording = False

        # Zone de conversation
        self.conversation_display = ctk.CTkTextbox(self, width=400, height=400)
        self.conversation_display.grid(row=0, column=0, rowspan=4, columnspan=4, padx=10, pady=10)
        self.conversation_display.configure(state="disabled")

        # Zone de texte pour l'envoi de messages
        self.user_input_var = ctk.StringVar(self, '')
        self.user_input = ctk.CTkEntry(self, textvariable=self.user_input_var, width=200, placeholder_text="Tapez votre message ici...")
        self.user_input.grid(row=4, column=0, padx=10, pady=10, sticky='W', columnspan=2)

        # Bouton pour envoyer le texte
        self.send_button = ctk.CTkButton(self, text="Envoyer", command=self.send_user_input, width=32, height=32, border_width=0, corner_radius=8, fg_color='grey')
        self.send_button.grid(row=4, column=2, padx=10, pady=10)

        # Bouton pour envoyer un vocal
        self.record_button = ctk.CTkButton(self, text="Démarrer l'enregistrement", command=self.record_button_callback, width=120, height=32, border_width=0, corner_radius=8, fg_color='grey')
        self.record_button.grid(row=4, column=3, padx=10, pady=10)

        # Case à cocher pour activer/désactiver l'audio
        self.audio_enabled = ctk.BooleanVar(value=True)
        self.audio_checkbox = ctk.CTkCheckBox(self, text="Activer la génération audio", variable=self.audio_enabled)
        self.audio_checkbox.grid(row=5, column=0, padx=10, pady=10, columnspan=2, sticky='W')

        # Bouton pour activer/désactiver la génération de l'audio
        self.toggle_audio_button = ctk.CTkButton(self, text="Désactiver la génération audio", command=self.toggle_audio_generation, width=200, height=32, border_width=0, corner_radius=8, fg_color='grey')
        self.toggle_audio_button.grid(row=6, column=0, padx=10, pady=10, columnspan=4, sticky='W')

    def send_user_input(self):
        user_message = self.user_input_var.get()
        self.user_input_var.set('')
        if user_message:
            self.display_message("Vous ", user_message)
            thread = Thread(target=self.get_bot_response, args=(user_message,), daemon=True)
            thread.start()

    def get_bot_response(self, user_message):
        response = get_chat_response(user_message)
        self.display_message("Amadeus ", response)
        if self.audio_enabled.get():
            audio_thread = Thread(target=text_to_speech, args=(response,), daemon=True)
            audio_thread.start()

    def record_button_callback(self):
        if self.isRecording:
            # Arrêter l'enregistrement
            self.record_button.configure(text="Démarrer l'enregistrement", fg_color='grey')
            self.isRecording = False
        else:
            # Démarrer l'enregistrement
            self.record_button.configure(text="Arrêter l'enregistrement", fg_color='#fc7b5b')
            self.isRecording = True
            thread = Thread(target=self.record_voice, daemon=True)
            thread.start()

    def record_voice(self):
        # Utiliser la fonction speech_to_text modifiée
        user_message = speech_to_text(self.is_recording)
        if user_message:
            self.display_message("Vous", user_message)
            thread = Thread(target=self.get_bot_response, args=(user_message,), daemon=True)
            thread.start()

    def is_recording(self):
        return self.isRecording


    
    def toggle_audio_generation(self):
        if self.audio_enabled.get():
            self.audio_enabled.set(False)
            self.toggle_audio_button.configure(text="Activer la génération audio", fg_color='grey')
        else:
            self.audio_enabled.set(True)
            self.toggle_audio_button.configure(text="Désactiver la génération audio", fg_color='grey')

    def display_message(self, sender, message):
        self.conversation_display.configure(state="normal")
        self.conversation_display.insert("end", f"{sender}: {message}\n")
        self.conversation_display.configure(state="disabled")
        self.conversation_display.see("end")

class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("490x600")
        self.title("Amadeus")
        self.resizable(False, False)

        # Conteneur de chat
        chat_frame = ChatFrame(master=self, width=600, height=600, bg_color='#f0f0f0')
        chat_frame.grid(row=0, column=0, padx=5, pady=20, sticky="nswe")

if __name__ == "__main__":
    app = ChatbotApp()
    app.configure(background='#fafafa')
    app.mainloop()
