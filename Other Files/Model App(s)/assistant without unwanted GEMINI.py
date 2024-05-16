import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
import pyautogui

# Set up the model
from huggingface_hub import InferenceClient

def format_prompt(message, history):
    prompt = ""
    for user_prompt, bot_response in history:
        prompt += f"[INST] {user_prompt} [/INST]"
        prompt += f" {bot_response} "
    prompt += f"[INST] {message} [/INST]"
    return prompt

def generate(prompt, history=[], temperature=0.9, max_new_tokens=256, top_p=0.95, repetition_penalty=1.0):
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        seed=42,
    )

    formatted_prompt = format_prompt(prompt, history)

    client = InferenceClient(model="mistralai/Mixtral-8x7B-Instruct-v0.1", token='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')
    stream = client.text_generation(formatted_prompt, **generate_kwargs, stream=True, details=True, return_full_text=False)
    output = ""

    for response in stream:
        output += response.token.text
    output = output.replace("<s>", "").replace("</s>", "")
    
    yield output
    return output
    

def gai(query):
    x=''
    for response in generate(query):
        x+=response
    return x

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

def speak(audio):
    engine.setProperty('voice', voices[1].id)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir !")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir !")
    else:
        speak("Good Evening Sir !")
    assname = "Jarvis 1 point o"
    speak("I am your Assistant")
    speak(assname)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"
    return query

if __name__ == '__main__':
    clear = lambda: os.system('cls')
    clear()
    wishMe()
    
    while True:
        assname = "Jarvis 1 point o"
        query = takeCommand().lower()
        if 'open youtube' in query:
            speak("Here you go to Youtube\n")
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            speak("Here you go to Google\n")
            webbrowser.open("google.com")
        
        elif 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("% H:% M:% S")
            speak(f"Sir, the time is {strTime}")
    
        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you, Sir")

        elif "what's your name" in query or "What is your name" in query:
            speak("My friends call me")
            speak(assname)
            print("My friends call me", assname)

        elif 'exit' in query:
            speak("Thanks for giving me your time")
            exit()

        elif "who made you" in query or "who created you" in query:
            speak("I have been created by Nafis Rayan.")

        elif 'search' in query or 'play' in query:
            query = query.replace("search", "")
            query = query.replace("play", "")
            webbrowser.open(query)
        
        elif "search in google" in query:
            query = query.replace("search in google", "")
            search = query
            speak("User asked for google to search")
            speak(search)
            webbrowser.open("https://www.google.com/search?q=" + search + "")

        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop jarvis from listening commands")
            a = int(takeCommand())
            time.sleep(a)
            print(a)
            speak("jarvis is now online again")

        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.com/maps/place/" + location + "")
        
        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Jarvis Camera ", "img.jpg")

        elif "take a screenshot" in query:
            img = pyautogui.screenshot()
            img.save("screenshot.png")

        elif "jarvis" in query:
            wishMe()
            speak("Jarvis 1 point o in your service Mister")
            speak(assname)

        # elif "weather" in query:
        #     query = query.replace("weather","")
        #     # result = weather.weather_report(query)
        #     # speak(result)
        #     print(result)

        elif "search in wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("search in wikipedia", "")
            results = wikipedia.summary(query, sentences = 3)
            speak("According to Wikipedia")
            speak(results)
            # webbrowser.open("wikipedia.com")

        elif "how are you" in query:
            speak("I'm fine, glad you me that")

        elif "i love you" in query:
            speak("thank you, smily face")
            
        elif "ask ai" in query:
            speak("Got it")
            query = query.replace("ask ai", "")
            output = gai(query).replace("</s>", "")
            print(output)
            speak(output)
			

#-----------------------------------------------Main Code Execution Ends Here ------------------------------------------
