from threading import Thread
from time import sleep

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageDraw


class Display:
    def __init__(self):
        serial0 = i2c(port=1, address=0x3C)
        self._display0 = sh1106(serial0)

    def write_teststuff_to_displays(self):
        with canvas(self._display0) as draw, canvas(self._display0) as draw:
            print(f"Type(draw) = {type(draw)} <><<<<<<<<<<<<<<<<<<")
            draw.text((0, 0), "Hi There", fill="white")
            draw.text((0, 0), "Hi There", fill="white")
        sleep(5)

    @property
    def dis0(self) -> ImageDraw.Draw:
        return self._display0

    def run_for_fun(self):
        print("hey")
