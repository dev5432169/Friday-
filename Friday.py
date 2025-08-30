#!/usr/bin/env python3

# Friday.py - Personal assistant and friend for Devansh Prabhakar

# Created by Devansh Prabhakar
import webbrowser
import random
import datetime
import subprocess
import sys
import importlib
import speech_recognition as sr
import pyttsx3
import torch
import requests
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

# 📦 Ensure required packages are installed
def install_packages():
    packages = {
        "speechrecognition": "speech_recognition",
        "pyaudio": "pyaudio",
        "requests": "requests",
        "transformers": "transformers",
        "torch": "torch",
        "pyttsx3": "pyttsx3"
    }
    for pkg, module in packages.items():
        try:
            importlib.import_module(module)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

install_packages()

# 🗣️ Friday's voice setup
def speak_friday(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
    engine.setProperty('rate', 175)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# 🧠 Devansh's profile
user_profile = {
    "name": "Devansh Prabhakar",
    "location": "Mumbai",
    "likes": ["coding", "space", "music"],
    "mood": "neutral"
}

reminders = []

# 👋 Friendly greeting
def greet_user():
    speak_friday(f"Hey {user_profile['name']}! I'm Friday, your assistant and friend. How can I brighten your day?")

# 🕰️ Date and time
def tell_date_time():
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %d %B %Y")
    time_str = now.strftime("%I:%M %p")
    message = f"Today is {date_str}, and it's {time_str}."
    print(message)
    speak_friday(message)

# 🌦 Weather report for any county/city
def get_weather():
    speak_friday("Which location would you like the weather for?")
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = recognizer.listen(source)
        try:
            location = recognizer.recognize_google(audio)
            print(f"Location: {location}")
            api_key = "your_openweathermap_api_key"  # Replace with your actual API key
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url).json()
            if response.get("cod") != 200:
                speak_friday("Sorry, I couldn't find that location.")
                return
            temp = response["main"]["temp"]
            condition = response["weather"][0]["description"]
            speak_friday(f"The temperature in {location} is {temp}°C with {condition}.")
        except:
            speak_friday("Sorry, I couldn't catch the location. Try again.")

            # 🌦 Weather report for any county/city
def get_weather():
    speak_friday("Sure! Which location would you like the weather for?")
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = recognizer.listen(source)
        try:
            location = recognizer.recognize_google(audio)
            print(f"Location requested: {location}")
            API_KEY = "your_openweathermap_api_key"  # Replace with your actual API key
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
            print(f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API_KEY}: {url}")
            Q = requests.get(url)

            if Q.get("cod") != 200:
                speak_friday(f"Sorry, I couldn't find weather data for {location}.")
                return

            temp = Q["main"]["temp"]
            feels_like = Q["main"]["feels_like"]
            humidity = Q["main"]["humidity"]
            wind = Q["wind"]["speed"]
            condition = Q["weather"][0]["description"].capitalize()

            weather_report = (
                f"In {location}, it's currently {temp}°C and feels like {feels_like}°C. "
                f"The sky is {condition}, humidity is at {humidity}%, and wind speed is {wind} meters per second."
            )
            print(weather_report)
            speak_friday(weather_report)

        except sr.UnknownValueError:
            speak_friday("Sorry, I couldn't catch the location. Could you repeat it?")
        except Exception as e:
            print(f"Weather error: {e}")
            speak_friday("Something went wrong while fetching the weather.")


# 🧠 Creative text generation
def ai_text_generation():
    generator = pipeline("text-generation", model="gpt2")
    prompt = "Today is Friday and AI can"
    result = generator(prompt, max_length=40, num_return_sequences=1)
    generated = result[0]['generated_text']
    print("AI generated:", generated)
    speak_friday("Here's something creative I came up with.")
    speak_friday(generated)

# 💬 Chat with Friday using DialoGPT
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
chat_history_ids = None

def talk_to_friday(user_input):
    global chat_history_ids
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    print(f"Friday: {response}")
    speak_friday(response)

# 🎯 Personal assistant features
def check_mood():
    mood = user_profile["mood"]
    if mood == "happy":
        speak_friday("I'm so glad you're feeling great! Want to hear a fun fact or a compliment?")
    elif mood == "sad":
        speak_friday("I'm here for you, Devansh. Want to talk about it or hear something uplifting?")
    else:
        speak_friday("Just cruising through the day? Let me know if you need anything.")

def give_compliment():
    speak_friday(f"{user_profile['name']}, you're brilliant and inspiring. I love how passionate you are about {user_profile['likes'][0]}!")

def set_reminder():
    speak_friday("What would you like me to remind you about?")
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = recognizer.listen(source)
        try:
            reminder = recognizer.recognize_google(audio)
            reminders.append(reminder)
            print(f"Reminder set: {reminder}")
            speak_friday(f"Got it! I'll remind you about: {reminder}.")
        except:
            speak_friday("Sorry, I couldn't catch that. Try again later.")

def cancel_reminder():
    if not reminders:
        speak_friday("You don't have any reminders to cancel.")
        return
    speak_friday("Which reminder would you like to cancel?")
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = recognizer.listen(source)
        try:
            to_cancel = recognizer.recognize_google(audio)
            if to_cancel in reminders:
                reminders.remove(to_cancel)
                speak_friday(f"Reminder '{to_cancel}' has been cancelled.")
            else:
                speak_friday("I couldn't find that reminder.")
        except:
            speak_friday("Sorry, I couldn't catch that.")

# 🎧 Listen and respond
def listen_for_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("🎙️ Friday is listening...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Say something...")
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                command = text.lower()

                if "friday" in command:
                    speak_friday("Hey! I'm here. What’s on your mind?")
                elif "time" in command or "date" in command:
                    tell_date_time()
                elif "weather" in command:
                    get_weather()
                elif "generate text" in command or "ai text" in command:
                    ai_text_generation()
                elif "talk to me" in command or "let's chat" in command or "i want to talk" in command:
                    speak_friday("Of course! I'm all ears. What do you want to talk about?")
                    audio = recognizer.listen(source)
                    user_input = recognizer.recognize_google(audio)
                    talk_to_friday(user_input)
                elif "how am i" in command or "check mood" in command:
                    check_mood()
                elif "compliment me" in command:
                    give_compliment()
                elif "set reminder" in command:
                    set_reminder()
                elif "cancel reminder" in command:
                    cancel_reminder()
                elif "thank you" in command or "thanks" in command:
                    speak_friday("You're welcome, Devansh. Always happy to help.")
                else:
                    speak_friday("I'm still learning. You can ask me the time, weather, set or cancel reminders, or just chat.")
            except sr.UnknownValueError:
                print("Didn't understand that.")
            except sr.RequestError as e:
                print(f"Recognition error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
                speak_friday("Oops, something went wrong.")

# 🚀 Start Friday
if __name__ == "__main__":
    greet_user()
    listen_for_commands()
# 🚀 Start Friday
openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": user_input}
    ]
)
def open_website(please_open):
    if "youtube" in please_open:
        speak_friday("Opening YouTube now.")
        webbrowser.open("https://www.youtube.com")
        return True
    elif "google" in please_open:
        speak_friday("Opening Google now.")
        webbrowser.open("https://www.google.com")
        return True
    return False

  # 🌦 Weather report for any city and country
def get_weather():
    speak_friday("Sure! Please say the city and country you'd like the weather for. For example, 'New York, United States' or 'Delhi, India'.")
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        location_input = recognizer.recognize_google(audio)
        print(f"Location requested: {location_input}")

        # 🔐 Replace with your actual OpenWeatherMap API key
        api_key = "your_openweathermap_api_key"
        if api_key == "your_openweathermap_api_key":
            speak_friday("Weather service is not configured properly. Please update your API key.")
            return

        # 🌐 Format location for API query
        location_query = location_input.strip().replace(" ", "+")  # '+' is more reliable for multi-word cities

        # 🛰️ Construct API request
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location_query}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        # ❌ Handle invalid location or API errors
        if data.get("cod") != 200:
            error_message = data.get("message", "Unknown error")
            speak_friday(f"Sorry, I couldn't find weather data for {location_input}. {error_message.capitalize()}.")
            return

        # ✅ Extract weather data
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        condition = data["weather"][0]["description"].capitalize()
        city_name = data["name"]
        country_code = data["sys"]["country"]

        # 📢 Speak the weather report
        weather_report = (
            f"In {city_name}, {country_code}, it's currently {temp}°C and feels like {feels_like}°C. "
            f"The sky is {condition}, humidity is {humidity}%, and wind speed is {wind} meters per second."
        )
        print(weather_report)
        speak_friday(weather_report)

    except sr.UnknownValueError:
        speak_friday("Sorry, I couldn't catch the location. Could you repeat it?")
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        speak_friday("There was a problem with speech recognition.")
    except requests.exceptions.RequestException as e:
        print(f"HTTP request error: {e}")
        speak_friday("I couldn't reach the weather service. Please check your internet connection.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        speak_friday("Something went wrong while fetching the weather.") 

    except Exception as e:
        print(f"Unexpected error: {e}")
        speak_friday("Oops, something went wrong.")

    finally:
        # Clean up resources or reset states if needed
        pass
print("Weather report process completed.")

from plyer import notification

def friday_notify(title="Friday Notification", message="Here's something you should know!"):
    notification.notify(
        title=title,
        message=message,
        app_name="Friday",
        timeout=8  # seconds
    )

# Example usage
if __name__ == "__main__":
    friday_notify("Weather Update", "It's 29°C in Mumbai with clear skies.")
from plyer import notification

def friday_notify(title="Friday Notification", message="Here's something you should know!"):
    notification.notify(
        title=title,
        message=message,
        app_name="Friday",
        timeout=8  # seconds
    )

# Example usage
if __name__ == "__main__":
    friday_notify("Weather Update", "It's 29°C in Mumbai with clear skies.")
  
