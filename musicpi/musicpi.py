from musicpi.hardware import RotaryEncoder, Display, Button, Led
from musicpi.mpd_wrapper import MpdWrapper

class MusicPi:
    def __init__(self) -> None:
        self._mpd