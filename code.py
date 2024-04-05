import sys
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os 
import google.generativeai as genai
import openai as ai
import re

#To use OpenAI's to fix the searching
apikey_openai = "MY OPEN AI KEY"
#Key hid for security reasons

#To use Googles's Gemini API to make the searching possible
genai.configure(api_key="API KEY")
#Key hid for security reasons
model = genai.GenerativeModel('gemini-pro')

#We are using SAPI5, which stands for  Speech Application Programming Interface Version 5.
#It is a Microsoft API that enables us to do speech recognition.
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 175)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def authenticate_user(spoken_passcode):
    stored_passcode = "Easy come easy go"

    try:
        print("Processing authentication...")
        speak("Processing Authentication")
        if spoken_passcode.lower() == stored_passcode.lower():
            print("Authentication successful.")
            speak("Authentication successful.")
            return True
        else:
            print("Authentication failed. Passcode does not match.")
            speak("Authentication failed. Passcode does not match.")
            return False
    except Exception as e:
        print("There was some error")
        speak("There was some error")
        return False

def wish(user):
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak(f"Good Morning, {user}.")
    elif 12 <= hour < 18:
        speak(f"Good Afternoon, {user}.")
    else:
        speak(f"Good Evening, {user}.")
    speak("How can I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f'User said : {query}')
        return query

    except Exception as e:
        print("I didn't get you, can you say that again?")
        speak("I didn't get you, can you say that again?")
        return "None"

def make_readable(text):
    pattern = r'[*_]'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

if __name__ == "__main__":
    speak("Hello! I am friday")
    print("Hello, I am F.R.I.D.A.Y")
    speak("Provide the passcode")
    print("Provide the passcode")
    passcode = takeCommand().lower()
    if(authenticate_user(passcode)):
        user = "Aditya"
        wish(user)
        while True:
            query = takeCommand().lower()

            if any(sentence in query for sentence in ["Hi Friday","hello friday","Hey there friday","yo friday"]):
                print(f"Hello {user}, F.R.I.D.A.Y here")
                speak(f"Hello {user}, friday here")

            elif "who are you" in query or "tell me about yourself" in query:
                speak("I am friday, an AI virtual assistant that is inspired from the Marvel Universe")
                speak("I have been created to do complex calculations, to make simulations and to make your life easier")

            elif any(sentence in query for sentence in ["what is","who is","how to", "how do I", "Write a", "We are having","Hey Friday,"]):
                try:
                    response_1 = model.generate_content(query)
                    response_2  = model.generate_content(response_1.text+'Make this smaller and simpler, but yet informative')
                    response=make_readable(response_2.text)
                    speak(response.text)
                    print(response.text)
                except:
                    speak("I am sorry, I couldn't find information on that")
                    print("I am sorry, I couldn't find information on that")


                #Intially we were using Wikipedia to search for whatever is asked.
                #But now as we are using the Gemini API to get our answers, the wikipedia string has been made as a doc string 
                #(just for the sake of it becoming a multiline comment)
                '''print("Searching Wikipedia...")
                if "what is" in query:
                    searchQuery = query.replace("what is ", "").strip()
                else:
                    searchQuery = query.replace("who is ", "").strip()

                try:
                    result = wikipedia.summary(searchQuery, sentences=2)
                    speak("According to Wikipedia...")
                    speak(result)
                    print(result)
                except wikipedia.exceptions.PageError:
                    speak("Sorry, I couldn't find information on that.")
                    print("Sorry, I couldn't find information on that.")
                except wikipedia.exceptions.DisambiguationError as e:
                    options = e.options
                    speak("The search query is ambiguous. Here are some options: " + ", ".join(options))
                    print("The search query is ambiguous. Here are some options: ", options)'''
                
            

            #Additional Operations
            elif "open my browser" in query or "open chrome" in query:
                speak("Starting Google Chrome")
                print("Opening Google Chrome")
                os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
            
            elif any(word in query for word in ["close chrome","close my browser","close browser"]):
                os.system("taskkill /f /im chrome.exe")
                speak("All Google Chrome windows have been closed")


            elif "open my code editor" in query or "open vs code" in query or "open visual studio code" in query:
                speak("Starting Visual Studio Code")
                print("Opening Visual Studio Code")
                os.startfile(r"C:\Users\{user} Pande\AppData\Local\Programs\Microsoft VS Code\Code.exe")

            elif any(sentence in query for sentence in ["shut down system","shut down","turn off"]):
                os.system("shutdown /s /t 5")
                speak("Turning off your PC. Goodbye!")
            
            elif any(sentence in query for sentence in ["restart system","restart","reboot"]):
                os.system("shutdown /r /t 5")

            elif any(sentence in query for sentence in ["lock system","lock my device","lock laptop"]):
                os.system("rundll32.exe  user32.dll,LockWorkStation")

            elif any(word in query for word in ["thank you", "thanks"]):
                speak("Your welcome")
                print("Your welcome")

            elif any(word in query for word in ["quit", "that's it", "stop ", "terminate", "abort"]):
                speak("Goodbye!")
                print("Goodbye!")
                sys.exit()

            

    else:
        speak("friday terminating")
        print("F.R.I.D.A.Y terminating")
