# Jarvis Voice Assistant

A voice-controlled AI assistant built with Python and Google Gemini.

## Features
- Wake word: say "Jarvis" to activate
- Understands natural commands like "launch YouTube" or "play skyfall"
- Opens websites and plays songs from a music library
- Reads sports news headlines
- Answers general questions using Gemini
- Follow-up mode: keeps listening without repeating the wake word

## Setup
1. Clone the repo and create a virtual environment: `python -m venv .venv`
2. Install packages: `pip install python-dotenv google-genai SpeechRecognition pyttsx3 PyAudio requests`
3. Create a `.env` file with your keys: