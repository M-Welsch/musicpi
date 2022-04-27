from musicpi.hmi import Hmi
from musicpi.hardware.pin_interface import Button, RotaryEncoder, Led
from musicpi.hardware.display import Display


class HmiArm(Hmi):
    def __init__(self) -> None:
        self._button = Button()
        self._led = Led()
        self._encoder = RotaryEncoder()
        self._display = Display()
