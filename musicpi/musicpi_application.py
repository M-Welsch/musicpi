from pathlib import Path
from time import sleep

from luma.core.render import canvas
from PIL import Image, ImageDraw, ImageFont

from musicpi import Mpd, SongInfo, Status
from musicpi.hmi.hmi import Hmi

icon_pause = Image.open(Path("musicpi/hmi/icons/pause.png"))
icon_play = Image.open(Path("musicpi/hmi/icons/play.png"))
icon_repeat = Image.open(Path("musicpi/hmi/icons/repeat.png"))
icon_no_repeat = Image.open(Path("musicpi/hmi/icons/no_repeat.png"))
icon_random = Image.open(Path("musicpi/hmi/icons/random.png"))
icon_no_random = Image.open(Path("musicpi/hmi/icons/no_random.png"))


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
        visualisation = Visualisation(display_content, status, song_info)
        visualisation.display_status()
        if song_info.title:
            ...
        else:
            canvas.text((0, 0), "empty playlist", fill="white", font=fnt)
        self._hmi.show_on_display(display_content)


class Visualisation:
    def __init__(self, display_content: Image, status: Status, song_info: SongInfo) -> None:
        self._display_content = display_content
        self._status: Status = status
        self._song_info: SongInfo = song_info
        self._canvas = ImageDraw.Draw(display_content)
        self._font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)

    def display_status(self) -> None:
        self._display_song_info()
        self._display_play_status()
        self._display_repeat()
        self._display_random()

    def _display_song_info(self) -> None:
        self._canvas.text((0, 11), self._song_info.artist, fill="white", font=self._font)
        self._canvas.text((0, 0), self._song_info.title, fill="white", font=self._font)

    def _display_play_status(self) -> None:
        self._display_content.paste(icon_play if self._status.playing else icon_pause, (0, 48))

    def _display_repeat(self) -> None:
        self._display_content.paste(icon_repeat if self._status.repeat else icon_no_repeat, (16, 48))

    def _display_random(self) -> None:
        self._display_content.paste(icon_random if self._status.random else icon_no_random, (32, 48))

    def _display_playlist_position(self) -> None:
        ...
