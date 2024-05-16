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

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
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
    
    while True:
        assname = "VAU 1 point o"
        query = takeCommand().lower()

        if "ask ai" in query:
            speak("Got it")
            query = query.replace("ask ai", "")
            output = gai(query).replace("</s>", "")
            print(output)
            speak(output)

#########################################################################################################

        elif "VAU" in query:
            speak(f"{assname} in your service Mister")

        elif "how are you" in query:
            speak("I'm fine, glad you asked me that")

        elif "i love you" in query:
            speak("thank you, smily face")
            
        elif "who made you" in query or "who created you" in query:
            speak("I have been created by Nafis Rayan.")

        elif "what's your name" in query or "What is your name" in query:
            speak("My friends call me")
            speak(assname)
            print("My friends call me", assname)

#########################################################################################################
        
        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop VAU from listening commands")
            a = int(takeCommand())
            time.sleep(a)
            print(a)
            speak("VAU is now online again")

        elif 'exit' in query:
            speak("Thanks for giving me your time")
            exit()

#########################################################################################################

        elif "search in google" in query:
            query = query.replace("search in google", "")
            search = query
            speak("User asked for google to search")
            speak(search)
            webbrowser.open("https://www.google.com/search?q=" + search + "")

        elif "search in wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("search in wikipedia", "")
            results = wikipedia.summary(query, sentences = 3)
            speak("According to Wikipedia")
            speak(results)
            # webbrowser.open("wikipedia.com")

#########################################################################################################
			

#-----------------------------------------------Main Code Execution Ends Here ------------------------------------------
