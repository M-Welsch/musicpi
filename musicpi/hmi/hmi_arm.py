from musicpi.hardware.display import Display
from musicpi.hardware.pin_interface import Button, Led, RotaryEncoder
from musicpi.hmi.hmi import Hmi


class HmiArm(Hmi):
    def __init__(self) -> None:
        self._button = Button()
        self._led = Led()
        self._encoder = RotaryEncoder()
        self._display = Display()
