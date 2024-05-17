import streamlit as st
import speech_recognition as sr
import pyttsx3
import winshell
import google.generativeai as genai
import wikipedia
import webbrowser
import time
from huggingface_hub import InferenceClient


# Set the background image
bg_image = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url(https://cdn.wallpapersafari.com/41/41/vIdSZT.jpg);
    background-size: cover;
}
</style>
"""

st.markdown(bg_image, unsafe_allow_html=True)

st.title("AI Voice Assistant")

Model = st.selectbox("Select your prefered model:", ["GEMINI", "MISTRAL8X", "PHI-3", "Custom Models"])

if Model == "GEMINI":
    tkey = st.text_input("Gemenai API key here:", "")

    # Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
    
    genai.configure(api_key=tkey)

    def gai(inp):
        return model.generate_content(inp).text

################################################################################################################

else:
    tkey = st.text_input("HuggingFace token here:", "")

    if Model == "MISTRAL8X":
        mkey= "mistralai/Mixtral-8x7B-Instruct-v0.1"
    elif Model == "PHI-3":
        mkey = "microsoft/Phi-3-mini-4k-instruct"
    else:
        mkey = st.text_input("Your HuggingFace Model String here:", "")

    def format_prompt(message, history):
        prompt = ""
        for user_prompt, bot_response in history:
            prompt += f"[INST] {user_prompt} [/INST]"
            prompt += f" {bot_response} "
        prompt += f"[INST] {message} [/INST]"
        return prompt

    def generate(prompt, history=[], temperature=0.9, max_new_tokens=1024, top_p=0.95, repetition_penalty=1.0):
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

        client = InferenceClient(model= mkey, token=tkey)
        stream = client.text_generation(formatted_prompt, **generate_kwargs, stream=True, details=True, return_full_text=False)
        output = ""

        for response in stream:
            output += response.token.text
        
        output = output.replace("<s>", "").replace("</s>", "")
        
        yield output
        return output


    # history = []
    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower() == "off":
    #         break
    #     history.append((user_input, "")) 
    #     for response in generate(user_input, history):
    #         print("Bot:", response)

    def gai(query):
        x=''
        for response in generate(query):
            x+=response
        return x

############################################################################################

show_commands = st.checkbox("Show Available Commands")

# List of commands
commands = [
    '"Ask AI [query]"',
    '"VAU in your service Mister"',
    '"How are you"',
    '"I love you"',
    '"Who made you"',
    '"What\'s your name"',
    '"Search in Google [query]"',
    '"Search in Wikipedia [query]"',
    '"Don\'t listen"',
    '"Exit"'
]

# Conditionally display the list of commands based on the checkbox state
if show_commands:
    st.header("Available Commands")
    st.write(commands)

############################################################################################

def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')

    engine.setProperty('voice', voices[1].id)
    engine.say(audio)
    engine.runAndWait()

# Create a speech recognition object
r = sr.Recognizer()

# Create a microphone object
mic = sr.Microphone()

st.write("Click the button and start speaking.")
button = st.button("Start")

# Define the function to transcribe the speech
def transcribe(audio):
    # recognize speech using Google Speech Recognition API
    try:
        text = r.recognize_google(audio)
        return text
    except sr.RequestError:
        return "API unavailable"
    except sr.UnknownValueError:
        return "Unable to recognize speech"

stop_button = st.button("Stop")
# Run the streamlit app
if button and not stop_button:
    with mic as source:
        # wait for a second to let the user adjust their microphone
        st.write("Adjusting microphone...")
        r.adjust_for_ambient_noise(source)
        st.write("Speak now!")
        speak("Speak now!")

        # start recording
        audio = r.listen(source)

        # transcribe the audio
        text = transcribe(audio)
        st.write(f"You said: {text}")

        speak(f"You said: {text}")
        speak(f"Give me a second.")

        assname = "VAU 1 point o"
        query = text.lower()
        

        if "ask ai" in query:
            speak("Got it")
            query = query.replace("ask ai", "")
            reply = gai(query)
            print(reply)

            st.write(f"Your reply:\n{reply}")
            reply = reply.replace('*','')
            speak(f"Your reply: {reply}")

#########################################################################################################

        elif "VAU" in query:
            speak(f"{assname} in your service Mister")
            st.write(f"{assname} in your service Mister")

        elif "how are you" in query:
            speak("I'm fine, glad you asked me that")
            st.write("I'm fine, glad you asked me that")

        elif "i love you" in query:
            st.write("thank you, smily face")

            
        elif "who made you" in query or "who created you" in query:
            speak("I have been made by Nafis Rayan.")
            st.write("I have been made by Nafis Rayan.")

        elif "what's your name" in query or "what is your name" in query:
            speak("My friends call me")
            speak(assname)
            print("My friends call me", assname)

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
        
        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop VAU from listening commands")
            audio = r.listen(source)
            a = int(transcribe(audio))
            time.sleep(a)
            print(a)
            speak("VAU is now online again")

        elif 'exit' in query:
            speak("Thanks for giving me your time")
            exit()
        
        else:
            speak("I did not get that, please try again")

#########################################################################################################
			

#-----------------------------------------------Main Code Execution Ends Here ------------------------------------------

        

