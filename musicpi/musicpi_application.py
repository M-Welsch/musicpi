from pathlib import Path
from time import sleep

from luma.core.render import canvas
from PIL import Image, ImageDraw, ImageFont

from musicpi import Mpd, SongInfo, Status
from musicpi.hmi.hmi import Hmi

icon_pause = Image.open(Path("musicpi/hmi/icons/pause.png"))


class MusicPi:
    def __init__(self, hmi: Hmi, cfg: dict) -> None:
        self._hmi = hmi
        self._cfg = cfg
        self._mpd = Mpd(cfg.get("mpd", {}))

    def start(self) -> None:
        while True:
            self.visualize_current_song()
            sleep(0.2)

    def visualize_current_song(self) -> None:
        song_info: SongInfo = self._mpd.current_song()
        status: Status = self._mpd.status()
        fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
        display_content = Image.new(mode="1", size=(128, 64), color=0)
        canvas = ImageDraw.Draw(display_content)
        if song_info.title:
            canvas.text((0, 11), song_info.artist, fill="white", font=fnt)
            canvas.text((0, 0), song_info.title, fill="white", font=fnt)
            if status.playing:
                ...
            else:
                playpause_icon = icon_pause
                display_content.paste(playpause_icon, (10, 20))

            if status.repeat:
                ...
            if status.random:
                ...

        else:
            canvas.text((0, 0), "empty playlist", fill="white", font=fnt)
        self._hmi.show_on_display(display_content)
