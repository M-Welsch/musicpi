from PIL import Image, ImageDraw
from signalslot import Signal


class Hmi:
    trigger_repeated_event = Signal()

    def start(self) -> None:
        raise RuntimeError("implement start-method in the respective hmi subclass!")

    def show_on_display(self, image: Image) -> None:
        raise RuntimeError("implement start-method in the respective hmi subclass!")

    @property
    def display(self) -> ImageDraw.Draw:
        raise RuntimeError("implement start-method in the respective hmi subclass!")

    @property
    def led(self):  # type: ignore
        ...

    @property
    def button_pressed(self) -> Signal:
        return Signal()

    @property
    def encoder_value_changed(self) -> Signal:
        return Signal()
