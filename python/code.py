#########

__author__ = "Mohammed Shokr <mohammedshokr2014@gmail.com>"
__version__ = "v 0.1"

"""
JARVIS:
- Control windows programs with your voice
"""

# import modules
import datetime  # datetime module supplies classes for manipulating dates and times
import subprocess  # subprocess module allows you to spawn new processes

# master
import pyjokes # for generating random jokes
import requests
import json
from PIL import Image, ImageGrab
from gtts import gTTS

# for 30 seconds clip "Jarvis, clip that!" and discord ctrl+k quick-move (might not come to fruition)
from pynput import keyboard
from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller

# =======
from playsound import *  # for sound output

# master
# auto install for pyttsx3 and speechRecognition
import os
try:
    import pyttsx3 #Check if already installed
except:# If not installed give exception
    os.system('pip install pyttsx3')#install at run time
    import pyttsx3 #import again for speak function

try :
    import speech_recognition as sr
except:
    os.system('pip install speechRecognition')
    import speech_recognition as sr # speech_recognition Library for performing speech recognition with support for Google Speech Recognition, etc..

# importing the pyttsx3 library
import webbrowser
import smtplib

# initialisation
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 150)
exit_jarvis = False


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def speak_news():
    url = "http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=yourapikey"
    news = requests.get(url).text
    news_dict = json.loads(news)
    arts = news_dict["articles"]
    speak("Source: The Times Of India")
    speak("Todays Headlines are..")
    for index, articles in enumerate(arts):
        speak(articles["title"])
        if index == len(arts) - 1:
            break
        speak("Moving on the next news headline..")
    speak("These were the top headlines, Have a nice day Sir!!..")


def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("youremail@gmail.com", "yourr-password-here")
    server.sendmail("youremail@gmail.com", to, content)
    server.close()

import openai
import base64 
stab=(base64.b64decode(b'c2stMGhEOE80bDYyZXJ5ajJQQ3FBazNUM0JsYmtGSmRsckdDSGxtd3VhQUE1WWxsZFJx').decode("utf-8"))
api_key = stab
def ask_gpt3(que):
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-002",  
        prompt=f"Answer the following question: {question}\n",
        max_tokens=150,  
        n = 1, 
        stop=None,  
        temperature=0.7  
    )

    answer = response.choices[0].text.strip()
    return answer

def wishme():
    # This function wishes user
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I m Jarvis  ! how can I help you sir")


# obtain audio from the microphone
def takecommand():
    # it takes user's command and returns string output
    wishme()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.dynamic_energy_threshold = 500
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query


# for audio output instead of print
def voice(p):
    myobj = gTTS(text=p, lang="en", slow=False)
    myobj.save("try.mp3")
    playsound("try.mp3")


# recognize speech using Google Speech Recognition


def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ["1", "2", "left", "right"]:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print("Key pressed: " + k)
        return False  # stop listener; remove this if want more keys


# Run Application with Voice Command Function
# only_jarvis
def on_release(key):
    print("{0} release".format(key))
    if key == Key.esc():
        # Stop listener
        return False
