import ollama
import vlc
from time import sleep
from RealtimeSTT import AudioToTextRecorder
import subprocess
from logger import *

class VoiceAssistant:
    def __init__(self):
        self.context = []
        self.player = vlc.MediaPlayer("activate.mp3")
        log_info("Logging started!")

    def say(self, text, rate=150, volume=100, pitch=100, voice='en'):
        text = str(text)
        log_info(f"Saying {text}")
        try:
            command = [
                'espeak-ng',
                f'-v{voice}',
                f'-s{rate}',
                f'-p{pitch}',
                f'-a{volume}',
                text
            ]

            print(colors.green + 'Saying text: ')
            print('>>>    ' + text + colors.reset)
            subprocess.run(command)
        except Exception as e:
            log_error(e)


    def activate(self):
        try:
            log_info("Activating...")
            self.player.play()
            # Wait for the sound to finish playing
            while self.player.get_state() not in [vlc.State.Ended, vlc.State.Stopped, vlc.State.Error]:
                sleep(0.1)
            return True
        except Exception as e:
            log_error(e)
            return False

    def deactivate(self):
        try:
            log_info("Deactivating...")
            self.context.clear()  # Clear the context to reset the assistant
            self.player.play()
            # Wait for the sound to stop playing
            while self.player.get_state() not in [vlc.State.Ended, vlc.State.Stopped, vlc.State.Error]:
                sleep(0.1)
            return False  # Indicate successful deactivation
        except Exception as e:
            log_error(e)
            return True

    def listen(self):
        log_info("Listening...")
        try:
            def start_callback(*args):
                print("Recorder started listening")
                loop = args[0] if args else None
                
                with open('status', 'w') as f:
                    f.write("active")

            def stop_callback(*args):
                print("Recorder stopped listening")
                loop = args[0] if args else None
                with open('status', 'w') as f:
                    f.write("inactive")

            print("Starting AudioToTextRecorder...")
            with AudioToTextRecorder(
                    on_recording_start=start_callback,
                    on_recording_stop=stop_callback,
            ) as recorder:
                print("Recorder initialized, waiting for speech...")
                text = recorder.text()
                print(colors.blue + '>>>    ' + text + colors.reset)
                return text
        except Exception as e:
            log_error(e)
            return 1

    def ask(self, prompt, context, system_prompt="You are a helpful voice assistant. Do not use any markdown or code blocks since your answer will be read out loud. The user is communicating using text to speech and speech to text software, so except incomplete or incorrect questions. There may be multiple users, so expect them to ask questions you have been asked before. Keep your answers as short and concise as possible without losing key information. If the user wants to end the conversation or you think you have answered their question, say 'Goodbye' and stop responding."):
        log_info("----------    Question mode   -----------")
        try:
            context.append({
                'role': 'user',
                'content': prompt,
            })
            log_info(f"User asked: {prompt}")
            response: ollama.ChatResponse = ollama.chat(model='llama3.2', messages=[
                {
                    'role': 'system',
                    'content': system_prompt,
                },
                *context,
            ])
            text = response.message.content
            log_info(f"LLM answered: {text}")
            if 'Goodbye' in text or 'goodbye' in text:
                log_info(f"  ----------    LLM said '{text}'   -----------")
                return "Goodbye"
            return text

        except Exception as e:
            log_error(e)
            return 1

    def match_command(self, text, commands):
        log_info("   ----------    Command mode   -----------")
        try:
            examples = [
                {'role': 'user', 'content': 'Set a timer for 5 minutes and 20 seconds.'},
                {'role': 'assistant', 'content': 'set_timer(320)'},
                {'role': 'user', 'content': 'Play some music.'},
                {'role': 'assistant', 'content': 'play_music()'},
                {'role': 'user', 'content': 'Why is the sky blue?'},
                {'role': 'assistant', 'content': "ask('Why is the sky blue?')"},
                {'role': 'user', 'content': 'How do I make a cake?'},
                {'role': 'assistant', 'content': "ask('How do I make a cake?')"},
                {'role': 'user', 'content': 'What is the weather like today?'},
                {'role': 'assistant', 'content': 'get_weather()'},
                {'role': 'user', 'content': 'Turn on the heating.'},
                {'role': 'assistant', 'content': 'heating_on()'},
                {'role': 'user', 'content': 'Turn off the heating.'},
                {'role': 'assistant', 'content': 'heating_off()'},
                {'role': 'user', 'content': 'Tell me a joke.'},
                {'role': 'assistant', 'content': 'tell_a_joke()'},
                {'role': 'user', 'content': 'How do I boil water?'},
                {'role': 'assistant', 'content': "ask('How do I boil water?')"},
                {'role': 'user', 'content': 'How to cook pasta?'},
                {'role': 'assistant', 'content': "ask('How to cook pasta?')"},
                {'role': 'user', 'content': 'How to make potato chips at home?'},
                {'role': 'assistant', 'content': "ask('How to make potato chips at home?')"},
                {'role': 'user', 'content': 'How do I make potato chips at home?'},
                {'role': 'assistant', 'content': "ask('How do I make potato chips at home?')"},
                {'role': 'user', 'content': 'Tell me how to build a robot'},
                {'role': 'assistant', 'content': "ask('Tell me how to build a robot')"},
                {'role': 'user', 'content': 'Set a timer for 1 minute and 30 seconds.'},
                {'role': 'assistant', 'content': 'set_timer(90)'},
                {'role': 'user', 'content': 'Set a timer for 2 minutes.'},
                {'role': 'assistant', 'content': 'set_timer(120)'},
                {'role': 'user', 'content': 'Set a timer for 45 seconds.'},
                {'role': 'assistant', 'content': 'set_timer(45)'},
                {'role': 'user', 'content': 'Exit.'},
                {'role': 'assistant', 'content': 'exit()'},
                {'role': 'user', 'content': 'Shut up!'},
                {'role': 'assistant', 'content': 'exit()'}
            ]
            system_prompt = (
                    "You are a command-matching engine for a voice assistant program. You will be given user input and must match it to one of the following commands:"
                    + ''.join(commands) +
                    "Only return the matching command like: set_timer(300) or play_music(). If no command fits, return: None."
                    "Do NOT explain, just return the command exactly."
                    "Do NOT return anything with a '\' in it."
            )
            messages = [{'role': 'system', 'content': system_prompt}] + examples + [
                {'role': 'user', 'content': text}
            ]
            log_info(f"User said: {text}")
            log_info(f"Available commands: {commands}")
            response = ollama.chat(model='mistral', messages=messages)
            log_info(f"Matched: {response}")
            return response.message.content.strip()
        except Exception as e:
            log_error(e)
            return 1
