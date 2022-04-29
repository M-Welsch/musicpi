from time import sleep

from luma.core.render import canvas
from PIL import Image, ImageDraw
from signalslot import Signal

from musicpi.hardware.display import Display
from musicpi.hardware.pin_interface import Button, Encoder, Led
from musicpi.hmi.hmi import Hmi


class HmiArm(Hmi):
    def __init__(self) -> None:
        self._button = Button()
        self._led = Led()
        self._encoder = Encoder()
        self._display = Display().dis

    def start(self) -> None:
        while True:
            self.trigger_repeated_event.emit()
            sleep(0.1)

    @property
    def display(self) -> ImageDraw.Draw:
        return self._display

    @property
    def led(self) -> Led:
        return self._led

    @property
    def encoder_value_changed(self) -> Signal:
        return self._encoder.val_changed

    @property
    def button_pressed(self) -> Signal:
        return self._button.sig_pressed

    def show_on_display(self, image: Image.Image) -> None:
        with canvas(device=self._display, background=image) as display:
            pass  # visualisation happens during __enter__
