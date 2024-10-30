# Alpha-Amadeus
L'alpha de Amadeus, un assistant virtuel basé sur la personnalité de **Kurisu Makise** dans **Steins;Gate**.

## Description
Alpha-Amadeus est un prototype d'assistant virtuel intégrant des éléments de reconnaissance vocale, génération de texte, et de lip-sync avec un avatar en temps réel. Ce projet vise à recréer une version immersive de l'IA Amadeus, inspirée par l'univers de Steins;Gate.

## Fonctionnalités
- **Interface graphique interactive** utilisant **customtkinter**.
- **Reconnaissance vocale** avec **SpeechRecognition** et conversion texte-voix avec **ElevenLabs**.
- **Réponses IA** générées par l'API **OpenAI**, avec la personnalité de Kurisu Makise.
- **Intégration VTube Studio** : Synchronisation des mouvements de bouche d'un avatar VTuber en fonction des réponses.

## Prérequis
- **Python 3.8+** : Assurez-vous d'avoir une version récente de Python installée.
- **Clés API** : Vous aurez besoin des clés API pour OpenAI, ElevenLabs, et VTube Studio.
- **VTube Studio** : Installé et configuré avec l'API activée.

## Installation
1. Clonez ce dépôt :
   ```sh
   git clone https://github.com/username/alpha-amadeus.git
   ```
2. Installez les dépendances depuis `requirements.txt` :
   ```sh
   pip install -r requirements.txt
   ```
3. Créez un fichier `.env` à la racine avec vos clés API (OpenAI, ElevenLabs, etc.).

## Configuration
- **.env** : Contient les informations de configuration suivantes :
  - `OPENAI_API_KEY` : Clé API pour l'API OpenAI.
  - `ELEVEN_API_KEY` : Clé API pour ElevenLabs.
  - `VTUBE_STUDIO_API_PORT` : Port de l'API VTube Studio (par défaut : 8001).
- **token.txt** : Contient le jeton d'authentification pour la connexion à VTube Studio.

## Fonctionnement
- **Interface graphique** : `interface.py` gère l'interface graphique de l'utilisateur, permettant d'envoyer des messages textuels ou vocaux.
- **Reconnaissance vocale et génération audio** : `voice.py` contient la logique de reconnaissance vocale et de synthèse audio.
- **Intégration avec VTube Studio** : `vtube.py` gère la connexion à VTube Studio et synchronise les mouvements de bouche de l'avatar.
- **Réponses générées par l'IA** : `gpt.py` utilise l'API OpenAI pour générer des réponses basées sur les messages de l'utilisateur.

## Utilisation
- Exécutez `interface.py` pour lancer l'interface graphique.
- Tapez un message ou utilisez la reconnaissance vocale pour interagir avec **Amadeus**.
- Observez l'avatar réagir et synchroniser les mouvements de bouche grâce à **VTube Studio**.

## Illustration
![image](https://github.com/user-attachments/assets/d8a37616-5042-4795-ae36-182bb3915f6b)

## Avertissement
Ce projet est une version alpha et est encore en cours de développement. Les éventuelles erreurs sont attendues et des contributions sont bienvenues.

## Crédits
- **Nythrox** : Développeur principal.
- Inspiré par **Steins;Gate**
Je me suis inspiré d'énormément de projet open source pour faire ce projet donc si jamais vous avez besoins que je vous cite dans les crédits si vous pensez que je me suis inspiré de vous n'hésitez pas à me le faire savoir !

