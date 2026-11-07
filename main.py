import speech_recognition as sr
import webbrowser
import pyttsx3
#import pocketsphinx
import musicLibrary
import requests
import json
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

recognizer = sr.Recognizer()
API_KEY = os.getenv("GNEWS_API_KEY")
SITES = {
    "google": "https://google.com",
    "facebook": "https://facebook.com",
    "youtube": "https://youtube.com",
    "instagram": "https://instagram.com",
}

ROUTER_PROMPT = """You are Jarvis, a voice assistant. Reply ONLY with JSON:
{"action": "open|play|news|chat", "target": "...", "reply": "..."}
- open: target is a site name (google, facebook, youtube, instagram)
- play: target is the song name
- news: target is empty
- chat: put a short 1-2 sentence spoken answer in "reply"

Examples:
"launch youtube" -> {"action": "open", "target": "youtube", "reply": ""}
"play skyfall" -> {"action": "play", "target": "skyfall", "reply": ""}
"tell me the news" -> {"action": "news", "target": "", "reply": ""}
"who is virat kohli" -> {"action": "chat", "target": "", "reply": "Virat Kohli is an Indian cricketer."}
"""

def parse_command(text):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=ROUTER_PROMPT,
            temperature=0.2,
            response_mime_type="application/json",
        ),
    )
    return json.loads(response.text)

def speak(text):
    print("Speaking:", text)
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def aiProcess(command):
      
     

     response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=command,
        config=types.GenerateContentConfig(
              system_instruction="You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Assistant. Keep your responses short and conversational, ideally 1-2 sentences, like a spoken assistant would answer — avoid long explanations, bullet points, or lists unless specifically asked for more detail."
         )
        
)

     return response.text

def conversation_mode():
    while True:
        with sr.Microphone() as source:
            print("listening for follow-up...")
            r.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                follow_up = r.recognize_google(audio)
                print(follow_up)

                if follow_up.lower() in ["stop", "exit", "quit", "goodbye"]:
                    speak("Okay, going back to sleep")
                    break

                procces_command(follow_up)
            except sr.WaitTimeoutError:
                speak("Going back to sleep")
                break
            except sr.UnknownValueError:
                speak("Sorry, I didn't catch that")
            except sr.RequestError:
                speak("Speech service is unavailable right now")

def procces_command(c):
    result = parse_command(c)
    action = result.get("action")
    target = result.get("target", "").lower().strip()

    if action == "open" and target in SITES:
        webbrowser.open(SITES[target])
    elif action == "play":
        link = musicLibrary.music.get(target)
        if link:
            webbrowser.open(link)
        else:
            speak("I don't have that song")
    elif action == "news":
        url = f"https://gnews.io/api/v4/top-headlines?category=sports&lang=en&country=in&max=5&apikey={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            for article in articles:
                speak(article["title"])

    else:
        output = result.get("reply") or aiProcess(c)
        speak(output)
            
    
          
   
if __name__== "__main__":
    speak("initializing jarvis")
    while True:
    # listen for the wake word 
    
    #obtain audio from the microphone 
    
     r = sr.Recognizer()


     print("recognizing")
#recognize speech using shpinx 
     try:
         with sr.Microphone() as source :
                 print("listening")
                 audio=r.listen(source,timeout=5,phrase_time_limit=3)
         word  =  r.recognize_google(audio) 
         if(word.lower() == "jarvis"):
             speak("ya")
             #this word is not hear after running  (error)            
             #listen for command
             with sr.Microphone() as source :
                 print("jarvis active")
                 r.adjust_for_ambient_noise(source, duration=1)

                 audio=r.listen(source, timeout=5,phrase_time_limit=5)
                 try:
                    command =  r.recognize_google(audio)
                    print(command)
                     
                    procces_command(command)
                    conversation_mode()
                 except sr.UnknownValueError:
                           speak("Sorry, I didn't catch that")
                 except sr.RequestError:
                           speak("Speech service is unavailable right now")   
                    

              
                              
     except Exception as e:
         print("error",e)






           

