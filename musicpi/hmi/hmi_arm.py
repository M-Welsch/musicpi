from luma.core.render import canvas
from PIL import Image, ImageDraw

from musicpi.hardware.display import Display
from musicpi.hardware.pin_interface import Button, Led, RotaryEncoder
from musicpi.hmi.hmi import Hmi


class HmiArm(Hmi):
    def __init__(self) -> None:
        self._button = Button()
        self._led = Led()
        self._encoder = RotaryEncoder()
        self._display = Display().dis

    def start(self) -> None:
        ...

    @property
    def display(self) -> ImageDraw.Draw:
        return self._display

    @property
    def led(self) -> Led:
        return self._led

    @property
    def encoder(self) -> RotaryEncoder:
        return self._encoder

    @property
    def button(self) -> Button:
        return self._button

    def show_on_display(self, image: Image.Image) -> None:
        with canvas(device=self._display, background=image) as display:
            pass  # visualisation happens during __enter__
