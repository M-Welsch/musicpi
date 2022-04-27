from musicpi import Mpd
from musicpi.hmi.hmi import Hmi


class MusicPi:
    def __init__(self, hmi: Hmi, cfg: dict) -> None:
        self._hmi = hmi
        self._cfg = cfg
        self._mpd = Mpd(cfg.get("mpd", {}))
