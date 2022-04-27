from threading import Thread
from time import sleep

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageDraw


class Display:
    def __init__(self) -> None:
        self._display = sh1106(i2c(port=1, address=0x3C))

    def write_teststuff_to_displays(self) -> None:
        with canvas(self._display) as draw:
            print(f"Type(draw) = {type(draw)} <><<<<<<<<<<<<<<<<<<")
            draw.text((0, 0), "Hi There", fill="white")
        sleep(5)

    @property
    def dis(self) -> ImageDraw.Draw:
        return self._display

    def run_for_fun(self) -> None:
        print("hey")
