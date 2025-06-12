import speech_recognition as sr
import time
import playsound
import random
import os
from gtts import gTTS
from time import ctime
import webbrowser
import pyjokes
import requests

r = sr.Recognizer()

def nocturna_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(f"Nocturna: {audio_string}")
    os.remove(audio_file)

def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            nocturna_speak(ask)
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5)
            voice_data = r.recognize_google(audio)
            print(f"You said: {voice_data}")
            return voice_data.lower()
        except sr.WaitTimeoutError:
            nocturna_speak("You were silent for too long. Try again.")
        except sr.UnknownValueError:
            nocturna_speak("Sorry, I did not understand that.")
        except sr.RequestError:
            nocturna_speak("Sorry, my speech service is down.")
        return ""

def get_weather(city):
    api_key = "b11c2697e0032062b761ff6a9411c391"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] != 200:
            return f"Sorry, I couldn't find the weather for {city}."
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city} is {weather} with a temperature of {temp}°C."
    except Exception:
        return "Sorry, I couldn't fetch the weather right now."

def respond(voice_data):
    if "what is your name" in voice_data:
        nocturna_speak("My name is Nocturna")
    elif "what time is it" in voice_data:
        nocturna_speak(ctime())
    elif "search" in voice_data:
        search = record_audio("What do you want to search for?")
        if search:
            url = "https://google.com/search?q=" + search
            webbrowser.get().open(url)
            nocturna_speak("Here’s what I found for " + search)
    elif "find location" in voice_data:
        location = record_audio("What location do you want to search for?")
        if location:
            url = "https://google.nl/maps/place/" + location
            webbrowser.get().open(url)
            nocturna_speak("Here’s the location for " + location)
    elif "Tell me a joke" in voice_data:
        joke = pyjokes.get_joke()
        nocturna_speak(joke)
    elif "find the weather" in voice_data:
        city = record_audio("which city do you want the weather for?")
        if city:
            weather_report = get_weather(city)
            nocturna_speak(weather_report)
    elif "note" in voice_data or "write" in voice_data or "take a note" in voice_data:
        note_content = record_audio("What would you like me to write?")
        if note_content:
            filename = f"note_{int(time.time())}.txt"
            with open(filename, "w") as f:
                f.write(note_content)
            nocturna_speak(f"I've saved your note as {filename}")

    elif "exit" in voice_data or "quit" in voice_data or "goodbye" in voice_data:
        nocturna_speak("Goodbye! Have a great day.")
        exit()
    elif voice_data.strip() == "":
        pass
    else:
        nocturna_speak("I’m still learning. Can you try another command?")

# Start
time.sleep(1)
nocturna_speak("Hello, how may I assist you today?")

while True:
    voice_data = record_audio()
    respond(voice_data)
