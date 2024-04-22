"""
ROBOT companion project
  - CircuitPython version 8

In this page we used 
  https://circuitpython.org/libraries
  - adafruit_requests.mpy - for http request of our API's

"""

import os
import wifi
import socketpool
import time
import microcontroller
import board
import adafruit_requests
import ssl
import json
from pomodoro import display_message, countdown_timer,alarm_countdown,generate_hour_keyboard,display_random_greeting
from music import play_connected,play_failure,play_pac,play_memories,play_shape_of_you,play_imagine_dragons_enemy,play_got,play_lion_sleeps_tonight,play_simpsons,play_nokia,play_tokyo,play_hello
import adafruit_hcsr04   #sonar
import gc
import random



# Get wifi details from a settings.toml file
# we developed a good habit of hiding sensitive information from the code and keep it in secured env.
print(os.getenv("test_env_file"))
ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")
telegrambot = os.getenv("botToken")

# Telegram API url.
API_URL = "https://api.telegram.org/bot" + telegrambot
update_id = 0  # Initialize update_id for telegram


def fetch_latest_update_id():
    global update_id
    get_url = API_URL + "/getUpdates?limit=1&offset=-1"  # Request the latest update
    r = requests.get(get_url)
    try:
        if r.json()['result']:
            update_id = r.json()['result'][0]['update_id']
    except (IndexError, KeyError):
        print("No new updates or error fetching the latest update_id")


def init_bot():
    get_url = API_URL
    get_url += "/getMe"
    r = requests.get(get_url)
    return r.json()['ok'] #returns bool value

def read_message(): #Relied on the Telegram Bot API documentation for this part, it is a well written documentation
    global update_id
    get_url = API_URL + "/getUpdates?limit=1&allowed_updates=[\"message\",\"callback_query\"]"
    get_url += "&offset={}".format(update_id + 1)

    r = requests.get(get_url)
    try:
        if r.json()['result']:
            update = r.json()['result'][0]
            update_id = update['update_id'] 
            if 'message' in update:
                message = update['message']['text']
                chat_id = update['message']['chat']['id']
                first_name = update['message']['from'].get('first_name', '')
                print(f"Message - Chat ID: {chat_id} Update_id: {update_id} Message: {message}")
                return chat_id, message, first_name, None  # Added a None here for consistency
            elif 'callback_query' in update:
                message = update['callback_query']['data']  # This is the data from the button.
                chat_id = update['callback_query']['message']['chat']['id']
                message_id = update['callback_query']['message']['message_id']
                print(f"Callback Query - Chat ID: {chat_id} Update_id: {update_id} Message: {message}")
                return chat_id, message, None, message_id  # message_id is needed for editing messages
    except (IndexError, KeyError):
        print("No new messages or error parsing response")
    return False, False, '', None


#sending message from telegram bot to the raspberry pi pico again Telegram Bot API
def send_message(chat_id, message, reply_markup=None): #sends message via chatid based on the message request
    get_url = API_URL
    get_url += "/sendMessage?chat_id={}&text={}".format(chat_id, message)
    if reply_markup is not None:
        get_url += "&reply_markup=" + reply_markup
    r = requests.get(get_url)
    
#connecting to wifi

print(f"Initializing...")
wifi.radio.connect(ssid, password)
print("connected!\n") #checked
play_connected()
pool = socketpool.SocketPool(wifi.radio)
print("IP Address: {}".format(wifi.radio.ipv4_address))
print("Connecting to WiFi '{}' ... ".format(ssid), end="") 
requests = adafruit_requests.Session(pool, ssl.create_default_context())


if init_bot() == False: #if bot initialization fails
    print("\nTelegram bot initialization failed.")
    play_failure()
else:
    print("\nTelegram bot ready!\n")
    play_connected()
    fetch_latest_update_id()

gc.collect()

#sonar loop
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP0, echo_pin=board.GP1)

while True:
    try:
        distance = sonar.distance
        #print(f"Distance: {distance} cm")
        if distance <= 10:
            play_hello()
            display_random_greeting(45,100)
            #print("Distance is less than or equal to 10 cm, breaking out to execute the loop.")
            break
    except RuntimeError as e:
        print("Failed to read distance:", e)
    time.sleep(1)

gc.collect()

while True:
    try: #if wifi connection fails, keeps on trying to reconnect
        while not wifi.radio.ipv4_address or "0.0.0.0" in repr(wifi.radio.ipv4_address): #Doc
            play_failure()
            print(f"Reconnecting to WiFi...")
            wifi.radio.connect(ssid, password) #Doc
            
        chat_id, message_in, user_name, message_id = read_message()
        if chat_id and message_in:
            gc.collect()
            if message_in == "/start":
                greet_msg = f"Hello {user_name}! Choose an option:"
                
                keyboard = {
                    "keyboard": [[{"text": "Study Mode"}, {"text": "Alarm Mode"}],[{"text": "Game Mode"}],[{"text": "Disco Mode"}]],
                    "resize_keyboard": True,
                    "is_persistent": True,
                }
                send_message(chat_id, greet_msg, reply_markup=json.dumps(keyboard))
            elif message_in == "Study Mode":
                play_connected()
                caption_text = "Unlock productivity with Pomodoro! Choose your focus journey!"
                inline_keyboard = {
                    "inline_keyboard": [
                        [{"text": "30' study - 5' break", "callback_data": "30-5"}],[{"text": "60' study - 10' break", "callback_data": "60-10"}],[{"text": "30'' study - 15'' break (demo)", "callback_data": "1-30"}]
                    ]
                }
                send_message(chat_id, caption_text, reply_markup=json.dumps(inline_keyboard))
                
            elif message_in == "30-5" and message_id:
                play_connected()
            # This is where you handle the callback for the inline keyboard
                send_message(chat_id, "Pomodoro timer confirmed for 30'- 5'. Tunnel vision!")
                countdown_timer(30,5)
                gc.collect()
            elif message_in == "60-10" and message_id:
                play_connected()
                send_message(chat_id, "Pomodoro timer confirmed for 60'- 10'. Tunnel vision!")
                countdown_timer(60,10)
                gc.collect()
                
                
            elif message_in == "1-30" and message_id:
                play_connected()
                send_message(chat_id, "Pomodoro timer confirmed for 30''- 15''. Tunnel vision!")
                countdown_timer(1,.5)
                caption_text = "You are doing great! Do you want to continue studying?"
                inline_keyboard = {
                    "inline_keyboard": [
                        [{"text": "YES", "callback_data": "Yes"}],[{"text": "NO", "callback_data": "No"}]
                    ]
                }
                display_message(caption_text,'/Bungee-Regular-26.bdf', 10, 20)
                send_message(chat_id, "Choose one: ", reply_markup=json.dumps(inline_keyboard))
                gc.collect()
                
            elif message_in == "Yes" and message_id:
                play_connected()
                gc.collect()
                countdown_timer(1,.5)
                caption_text = "You are doing great! Do you want to continue studying?"
                inline_keyboard = {
                    "inline_keyboard": [
                        [{"text": "YES", "callback_data": "Yes"}],[{"text": "NO", "callback_data": "No"}]
                    ]
                }
                display_message(caption_text,'/Bungee-Regular-26.bdf', 10, 20)
                send_message(chat_id, "Choose one: ", reply_markup=json.dumps(inline_keyboard))
                gc.collect()
                
            elif message_in == "No" and message_id:
                keyboard = {
                    "keyboard": [[{"text": "Study Mode"}, {"text": "Alarm Mode"}],[{"text": "Game Mode"}],[{"text": "Disco Mode"}]],
                    "resize_keyboard": True,
                    "is_persistent": True,
                }
                time.sleep(1)
                play_connected()
                display_message("What do you wanna do?",'/Bungee-Regular-26.bdf', 50, 100)
                send_message(chat_id, "Choose one form the main menu: ", reply_markup=json.dumps(keyboard))
                gc.collect()
                
            elif message_in == "Game Mode":
                gc.collect()
                play_pac()
                caption_text = "Glad, you want to have some fun, Lets goooo!"
                inline_keyboard = {
                    "inline_keyboard": [
                        [{"text": "Play XO", "callback_data": "XO"}],[{"text": "Play Would You Rather", "callback_data": "WYR"}],
                    ]
                }
                display_message(caption_text,'/Bungee-Regular-26.bdf', 10, 20 )
                gc.collect()
                send_message(chat_id, "Choose One: ", reply_markup=json.dumps(inline_keyboard))
                
            elif message_in == "WYR" and message_id:
                play_connected()
                with open('wrq.txt', 'r') as file:
                    questions = [q.strip() for q in file.readlines() if q.strip()]
                question_index = random.randint(0, len(questions) - 1)
                last_question_index = question_index  # Store the index of the chosen question
                question = questions[question_index]
                parts = question.split('Would you rather ')[1].split(' or ')
                choice1, choice2 = parts[0].strip(), parts[1].replace('?', '').strip()

                inline_keyboard = {
                    "inline_keyboard": [[{"text": choice1, "callback_data": "answer"}],
                                        [{"text": choice2, "callback_data": "answer"}],
                                        [{"text": "Play Again!", "callback_data": "WYR"}]]
                }
                display_message(question,'/Bungee-Regular-26.bdf', 10, 20)
                send_message(chat_id, "Choose one: ", reply_markup=json.dumps(inline_keyboard))
                play_connected()
                gc.collect()
                
            elif message_in in "answer":  # User makes a choice.
                play_connected()
                if last_question_index is not None:
                    with open('ans.txt', 'r') as ans_file:
                        answers = [a.strip() for a in ans_file.readlines()]
                        computer_answer = answers[last_question_index]
                    #send_message(chat_id, "Computer's choice: " + computer_answer)
                    display_message(computer_answer,'/Bungee-Regular-26.bdf', 10, 20)
                gc.collect()
            
            elif message_in == "Disco Mode":
                play_connected()
                caption_text = "They call me Michael Robo Jackson! Let's go wild Jammin'"
                # Define all your music functions for easy reference
                music_functions = {
                    "Memories": "play_memories",
                    "Shape of You": "play_shape_of_you",
                    "Imagine Dragons": "play_imagine_dragons_enemy",
                    "Game of Thrones": "play_got",
                    "Lion Sleeps Tonight": "play_lion_sleeps_tonight",
                    "The Simpsons": "play_simpsons",
                    "Tokyo Drift" : "play_tokyo"
                }
                # Generate inline keyboard based on the music functions
                inline_keyboard = {
                    "inline_keyboard": [[{"text": name, "callback_data": func}] for name, func in music_functions.items()]
                }
                display_message(caption_text, '/Bungee-Regular-26.bdf', 10, 20)
                send_message(chat_id, "Select a tune:", reply_markup=json.dumps(inline_keyboard))
                gc.collect()


            elif "play_" in message_in:  # Checking if the callback data is for playing a song
                function_to_call = message_in  # The callback data itself is the function name
                if function_to_call in globals():  # Check if function exists in the current global scope
                    globals()[function_to_call]()  # Call the function dynamically
                    display_message("Oww, done playing, let's go again!", '/Bungee-Regular-26.bdf', 10, 20)
                    play_connected()                

                else:
                    play_failure()
                    display_message("Sorry, I can't find that tune.", '/Bungee-Regular-26.bdf', 10, 20)
                    send_message(chat_id, "Sorry, I can't find that tune.")

        

            elif message_in == "Alarm Mode":
                gc.collect()
                play_connected()
                caption_text = "Set alarm time. First, choose hours from now:"
                inline_keyboard_hours = {
                    "inline_keyboard": generate_hour_keyboard()
                }
                display_message(caption_text,'/Bungee-Regular-26.bdf', 10, 20)
                send_message(chat_id, "Hours from now: ", reply_markup=json.dumps(inline_keyboard_hours))
                gc.collect()
            
            elif "hour_" in message_in:
                gc.collect()
                play_connected()
                selected_hour = int(message_in.split('_')[1])  # Parse the selected hour
                caption_text = f"Hour set to {selected_hour}. Now, choose minutes:"
                inline_keyboard_minutes = {
                    "inline_keyboard": [[{"text": f"{m}''", "callback_data": f"minute_{m}"} for m in range(0, 60, 10)]]
                }
                display_message(caption_text,'/Bungee-Regular-26.bdf', 10, 20)
                send_message(chat_id, "Choose minutes:", reply_markup=json.dumps(inline_keyboard_minutes))
                gc.collect()

            elif "minute_" in message_in:
                gc.collect()
                selected_minute = int(message_in.split('_')[1])  # Parse the selected minute
                send_message(chat_id, f"Alarm set for {selected_hour} hours and {selected_minute} minutes. However, this is for demo 30''")
                #alarm_countdown(selected_hour, selected_minute)
                alarm_countdown(0, .5)
                time.sleep(1)
                play_connected()
                display_message("What do you wanna do?",'/Bungee-Regular-26.bdf', 50, 100)
                gc.collect()
                

            else:
                send_message(chat_id, "Command is not available.")
                play_failure()
                display_message("Sry Pal","/Bungee-Regular-52.bdf", 50, 100)
                gc.collect()
        
        else:
            time.sleep(1)
        
    except OSError as e: #catching errors wohhooo! lol
        print("Failed!\n", e)
        play_failure()
        microcontroller.reset()
