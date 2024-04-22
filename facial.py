import board
import busio
import displayio
import adafruit_ili9341
import time
import random
from adafruit_display_shapes.rect import Rect

displayio.release_displays()

# Initialize the display
spi_pins = [board.GP11, board.GP10, board.GP17, board.GP18, board.GP16]
spi = busio.SPI(clock=spi_pins[1], MOSI=spi_pins[0])
display_bus = displayio.FourWire(spi, command=spi_pins[4], chip_select=spi_pins[3], reset=spi_pins[2])
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

# Colors
WHITE = 0xFFFFFF
BLACK = 0x000000

face_group = displayio.Group()
face = Rect(0, 0, 320, 240, fill=WHITE, outline=BLACK, stroke=0)
    #face = Rect(60, 40, 200, 160, fill=WHITE, outline=BLACK, stroke=5)
face_group.append(face)

    # Constants for eye geometry
eye_width = 50
eye_x1 = 50 #100
eye_x2 = 220 #170
eye_y_open = 90
eye_y_closed = 110
eye_height_open = 30
eye_height_closed = 1

    # Initial state: eyes open
eye1 = Rect(eye_x1, eye_y_open, eye_width, eye_height_open, fill=BLACK)
eye2 = Rect(eye_x2, eye_y_open, eye_width, eye_height_open, fill=BLACK)

face_group.append(eye1)
face_group.append(eye2)

display.show(face_group)
    

# Blinking loop with random intervals
def facialfit():
    # Create the robot face background

    while True:
        # Determine random time intervals for blinking
        time_open = random.uniform(1, 5)  # Eyes open for 1 to 5 seconds
        time_closed = random.uniform(0.1, 0.5)  # Eyes closed for 0.1 to 0.5 seconds

        time.sleep(time_open)  # Wait for a random time with eyes open

        # Close eyes
        face_group.pop()
        face_group.pop()

        eye1_closed = Rect(eye_x1, eye_y_closed, eye_width, eye_height_closed, fill=BLACK)
        eye2_closed = Rect(eye_x2, eye_y_closed, eye_width, eye_height_closed, fill=BLACK)

        face_group.append(eye1_closed)
        face_group.append(eye2_closed)
        display.show(face_group)

        time.sleep(time_closed)  # Wait for a random time with eyes closed

        # Open eyes
        face_group.pop()
        face_group.pop()

        eye1_open = Rect(eye_x1, eye_y_open, eye_width, eye_height_open, fill=BLACK)
        eye2_open = Rect(eye_x2, eye_y_open, eye_width, eye_height_open, fill=BLACK)

        face_group.append(eye1_open)
        face_group.append(eye2_open)
        display.show(face_group)

facialfit()