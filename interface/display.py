import board
import busio
import digitalio
from PIL import Image, ImageDraw
import adafruit_rgb_display.st7789 as st7789
import logging

class Display:
    """
    Class responsible for initializing and managing the display hardware.
    """

    def __init__(self):
        try:
            # Pin configuration
            self.cs_pin = digitalio.DigitalInOut(board.CE0)
            self.dc_pin = digitalio.DigitalInOut(board.D24)
            self.reset_pin = digitalio.DigitalInOut(board.D25)

            # Display properties
            self.baudrate = 32000000
            self.width = 170
            self.height = 320

            # SPI interface initialization
            self.spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

            # Create display object
            self.disp = st7789.ST7789(
                self.spi,
                cs=self.cs_pin,
                dc=self.dc_pin,
                rst=self.reset_pin,
                baudrate=self.baudrate,
                width=self.width,
                height=self.height,
                x_offset=35,
                y_offset=0,
                rotation=180
            )

            # Backlight (BLK) configuration
            self.backlight = digitalio.DigitalInOut(board.D18)
            self.backlight.direction = digitalio.Direction.OUTPUT
            self.backlight.value = True  # Turn on backlight

            # Create image object
            if self.disp.rotation in (90, 270):
                self.image = Image.new("RGB", (self.disp.height, self.disp.width))
            else:
                self.image = Image.new("RGB", (self.disp.width, self.disp.height))

            # Create drawing object
            self.draw = ImageDraw.Draw(self.image)

        except Exception as e:
            logging.error(f"Error initializing display: {e}", exc_info=True)
            raise