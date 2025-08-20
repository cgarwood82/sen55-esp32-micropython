"""ILI9488 demo (fonts)."""
from ili9488 import Display, color565


def test():
    """Test code."""
    # Baud rate of 60000000 seems about the max
    spi = SPI(1, baudrate=60000000, sck=Pin(2), mosi=Pin(7))
    display = Display(spi, dc=Pin(10), cs=Pin(8), rst=Pin(4))

    print('Loading fonts...')
    print('Loading arcadepix')
    arcadepix = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)
    print('Loading bally')
    bally = XglcdFont('fonts/Bally7x9.c', 7, 9)

    display.draw_text(0, 0, 'transmutated is a HACK!!', arcadepix, color565(0, 0, 255))
    display.draw_text(0, 22, 'nebur99 was here', bally, color565(0, 255, 0))
    for i in range(480):
        display.draw_pixel(160, i, color565(255, 0, 0))
test()

==========================
import random
import time
from machine import SPI, Pin
import ili9488  # Assuming you're using the ILI9488 driver
from xglcd_font import XglcdFont  # Adjust import if needed

# Set our screen variables
rotation=0
disp_width=480
disp_height=320
# Initialize SPI and display (update pins as needed)
spi = SPI(1, baudrate=60000000, sck=Pin(2), mosi=Pin(7))
display = ili9488.Display(spi, dc=Pin(10), cs=Pin(8), rst=Pin(4), rotation=0, width=disp_width, height=disp_height)

# Load a font (update font path and dimensions as needed)
font = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)

def color565(r, g, b):
    """Convert 8-bit RGB values to 16-bit 565 color."""
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

def draw_random_text(display, font, text, width, height, count=20):
    for _ in range(count):
        # Generate random position
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        # Generate a random color
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = color565(r, g, b)
        # Draw the text at the random position and color
        display.draw_text(x, y, text, font, color)

# Optionally, if you want it to update repeatedly:
while True:
    draw_random_text(display, font, "Nebur99 was here", disp_width, disp_height)
    draw_random_text(display, font, "transmutated is a hack", disp_width, disp_height)
    time.sleep(2)  # Wait a couple of seconds before redrawing
