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

def procces_command(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
            webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
                webbrowser.open("https://youtube.com")
    elif "open instagram" in c.lower():
                    webbrowser.open("https://instagram.com")            
    elif c.lower().startswith("play"):
          song=c.lower().split(" ")[1]
          link = musicLibrary.music[song]
          webbrowser.open(link)
   
    elif "news" in c.lower():
         url = f"https://gnews.io/api/v4/top-headlines?category=sports&lang=en&country=in&max=5&apikey={API_KEY}"
         response = requests.get(url)
         if response.status_code == 200:
                data = response.json()  #dont say play new , say other then this say any sentance that includes news like " tell me the news "
                #phrase the json response
                articles = data.get("articles",[])

                #print the headlines 
                for article in articles:
                      speak(article["title"])

    else:
          #let open ai handle the request   
          output = aiProcess(c)
          speak(output)   

          # conversation mode - keep talking without needing "jarvis" again
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
                                  break # exits conversation mode, back to wake-word loop

                           output = aiProcess(follow_up)
                           speak(output)
                        except sr.UnknownValueError:
                            speak("Sorry, I didn't catch that")
                        except sr.RequestError:
                             speak("Speech service is unavailable right now")   
            
    
          
   
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
                 except sr.UnknownValueError:
                           speak("Sorry, I didn't catch that")
                 except sr.RequestError:
                           speak("Speech service is unavailable right now")   
                    

              
                              
     except Exception as e:
         print("error",e)






           

