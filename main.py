import assistant
import colors
import random
import time
import threading
import requests as rq
import homeassistant
from logger import *


def play_music():
    print("Playing music...")

def tell_a_joke():
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "Why don't skeletons fight each other? They don't have the guts!",
        "What do you call cheese that isn't yours? Nacho cheese!",
        "Why did the math book look sad? Because it had too many problems!"
    ]
    va.say(random.choice(jokes))

def set_timer(seconds):
    seconds = int(seconds)
    def timer_done():
        va.say("Time's up!")

    timer_thread = threading.Timer(seconds, timer_done)
    timer_thread.start()

def heating_on():
    homeassistant.heating_on()

def heating_off():
    homeassistant.heating_off()

def get_weather():
    try:
        with open("OPENWEATHER_API_KEY", "r") as file:
            key = file.read().strip()
        city_name = "Ardcost"
        state_code = "Kerry"
        country_code = "IE"
        limit = "1"

        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={limit}&appid={key}"
        response = rq.get(url)
        data = response.json()
        lat = data[0]['lat']
        lon = data[0]['lon']

        url = (f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=metric")
        response = rq.get(url)
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        wind_speed = data['wind']['speed']
        humidity = data['main']['humidity']

        va.say(f"The weather is {weather_description} with a temperature of {temperature}°Celsius. The wind speed is {wind_speed} meters per second and the humidity is {humidity}%.")
    except Exception as e:
        print(colors.red + "Error fetching weather data: " + colors.reset)
        print("")
        print("")
        print(f"{colors.cyan}{e}{colors.reset}")


def ask(question):
    context = []
    response = va.ask(question, context)
    context.append({'role': 'user', 'content': question})
    context.append({'role': 'assistant', 'content': response})
    va.say(response)
    start_time = time.time()
    while True:
        try:
            text = va.listen()
            response = va.ask(text, context)
            context.append({'role': 'user', 'content': text})
            context.append({'role': 'assistant', 'content': response})
            va.say(response)
            start_time = time.time() # Reset the timer after each response
            if response == "Goodbye":
                break
        except Exception as e:
            print(colors.yellow + str(e) + colors.reset)
            return False

if __name__ == "__main__":
    va = assistant.VoiceAssistant()
    active = False
    wakeword = "Hey Google"
    print(wakeword)
    commands = [
        "play_music()",
        "tell_a_joke()",
        "set_timer(seconds)",
        "get_weather()",
        "heating_on()",
        "heating_off()",
        "ask('question')",
        "exit()"
    ]


    while True:
        while not active:
            print(f"{colors.purple} not active {colors.reset}")
            text = va.listen()
            if text == 1:
                print("Error, continue")
                continue
            elif wakeword in text or wakeword.capitalize() in text:
                active = va.activate()

        while active:
            print(f"{colors.purple} active {colors.reset}")

            text = va.listen()
            if text != 1:
                command = va.match_command(text, commands)
                if command != 1:
                    command = command.replace(r"\_", "_")
                    print(command)
                    if command not in commands and not command.startswith("ask(") and not command.startswith("set_timer("):
                        print("Invalid command:", command)
                        continue
                    elif command.startswith("exit("):
                        active = va.deactivate()
                    else:
                        try:
                            eval(command)
                        except Exception as e:
                            log_error(f"Error executing command {command}: {e}")
                            continue
                else:
                    log_error("Error in command matching")
            if "shutdown" in text or "Shut down" in text or "shut down" in text or "Shutdown" in text:
                print("Shutting down...")
                exit()
