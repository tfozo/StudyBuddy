import time
import board
import busio
import displayio
import adafruit_ili9341
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import audiomp3
import audiopwmio
import gc
import random
from music import play_study, play_break, play_memories,play_connected



displayio.release_displays()
# Board configuration
spi_pins = [board.GP11, board.GP10, board.GP17, board.GP18, board.GP16]
spi = busio.SPI(clock=spi_pins[1], MOSI=spi_pins[0])
display_bus = displayio.FourWire(spi, command=spi_pins[4], chip_select=spi_pins[3], reset=spi_pins[2])
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)



main_group = displayio.Group()
#display.show(main_group)



def display_message(message, font_path, x=0, y=0, line_spacing=5):
    
    while len(main_group) > 0:
        main_group.pop()

    # Set background to black
    background = displayio.Bitmap(320, 240, 1)  # Screen dimensions for ILI9341
    palette = displayio.Palette(1)
    palette[0] = 0x000000  # Background color black
    bg_sprite = displayio.TileGrid(background, pixel_shader=palette)
    main_group.append(bg_sprite)

    font = bitmap_font.load_font(font_path)
    
    screen_width = 320  # Screen width for ILI9341
    max_chars_per_line = screen_width // 20  # Adjust based on font and screen
    
    words = message.split(' ')
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars_per_line:
            current_line += (word + " ")
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())

    y_offset = y
    for line in lines:
        # Generate a random color for each line of text
        text_color = random.randint(0, 0xFFFFFF)
        text_area = label.Label(font, text=line, color=text_color)
        text_area.x = x
        text_area.y = y_offset
        main_group.append(text_area)
        y_offset += text_area.bounding_box[3] + line_spacing

    # Refresh the display with the updated group
    #display.show(main_group)
    gc.collect()



def countdown_timer(main_duration=.5, break_duration=.25):
    # Play the sound before starting the countdown
    gc.collect()
    session_sounds = [play_study, play_break] 
    session_labels = ['study', 'break']
    large_font = bitmap_font.load_font("/Bungee-Regular-52.bdf")

    for index, duration in enumerate([main_duration, break_duration]):
        session_sounds[index]()
        countdown_group = displayio.Group()
        display.show(countdown_group)
        end_time = time.monotonic() + duration * 60

        # Create and display the session label
        session_text_area = label.Label(large_font, text=session_labels[index], color=0xFFFFFF)
        session_text_area.x = (display.width // 8) + 30
        session_text_area.y = display.height - 160
        countdown_group.append(session_text_area)
        gc.collect()
        while time.monotonic() < end_time:
            remaining = int(end_time - time.monotonic())
            mins, secs = divmod(remaining, 60)
            time_str = '{:02d}:{:02d}'.format(mins, secs)

            # Update the timer display
            text_area = label.Label(large_font, text=time_str, color=0xFFFFFF)
            text_area.x = display.width // 8 + 35
            text_area.y = display.height - 100
            while len(countdown_group) > 1:
                countdown_group.pop(1)
            countdown_group.append(text_area)
            display.refresh()
            gc.collect()
    while len(countdown_group) > 0:
        countdown_group.pop()

    # Since countdown_group was the last active group shown, now we can switch back safely
    display.show(main_group)  # Transition back to main_group

#countdown_timer(.3,.3)

def alarm_countdown(hours, minutes):
    gc.collect()
    countdown_group = displayio.Group()
    display.show(countdown_group)
    play_connected()
    total_seconds = (hours * 3600) + (minutes * 60)
    end_time = time.monotonic() + total_seconds
    large_font = bitmap_font.load_font("/Bungee-Regular-52.bdf")

    # Initialize with a placeholder time text
    time_area = label.Label(large_font, text='00:00:00', color=0xFFFFFF)
    time_area.x = 40  # Adjust position based on your display size
    time_area.y = 120  # Adjust position based on your display size
    countdown_group.append(time_area)

    while time.monotonic() < end_time:
        remaining = int(end_time - time.monotonic())
        hrs, remainder = divmod(remaining, 3600)
        mins, secs = divmod(remainder, 60)
        time_str = '{:02d}:{:02d}:{:02d}'.format(hrs, mins, secs)

        if time_area.text != time_str:
            # Only update the time text if it has changed
            time_area.text = time_str
            display.refresh()

        gc.collect()

    # Clear the countdown display and play end sound
    while len(countdown_group) > 0:
        countdown_group.pop()

    play_memories()
    gc.collect()
    display.show(main_group)

#alarm_countdown(0,.1)

def generate_hour_keyboard():
    inline_keyboard = []
    row = []
    for hour in range(24):  # Adjust the range if you want fewer hours
        row.append({"text": f"{hour} hr", "callback_data": f"hour_{hour}"})
        if (hour + 1) % 6 == 0 or hour == 23:  # Adjust the split for fewer columns per row
            inline_keyboard.append(row)
            row = []
    return inline_keyboard



def display_random_greeting(x, y, font_path="/Bungee-Regular-26.bdf", screen_width=320, line_spacing=5, randomness=True):

    gc.collect()

    # Load the specified font
    font = bitmap_font.load_font(font_path)

    # Create a new group for this message
    text_group = displayio.Group()

    # Select either a random greeting or the specific message "XYZ"
    message = "^_^"
    if randomness:
        greetings = [
            "Hey there! Long time no see!",
            "Look who's here! Missed you!",
            "What a pleasant surprise!",
            "It's been too long, my friend!",
            "Hey! How have you been?",
            "You've been missed!",
            "So glad to see you again!",
            "Where have you been hiding?",
            "Back and better than ever!",
            "There's my favorite person!"
        ]
        message = random.choice(greetings)

    # Determine max number of characters per line based on screen width and font size
    max_chars_per_line = screen_width // 20

    # Split message into words and construct lines
    words = message.split(' ')
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars_per_line:
            current_line += (word + " ")
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())

    # Display each line on the screen with a random color
    y_offset = y
    for line in lines:
        text_color = random.randint(0, 0xFFFFFF) if randomness else 0x00ABFF  # Conditional color based on randomness
        text_area = label.Label(font, text=line, color=text_color)
        text_area.x = x
        text_area.y = y_offset
        text_group.append(text_area)
        y_offset += text_area.bounding_box[3] + line_spacing

    # Show the text group on the display
    display.show(text_group)

    gc.collect()
    return text_group
#display_random_greeting(45,100)
display_random_greeting(100,100,font_path="/Bungee-Regular-52.bdf",randomness=False)