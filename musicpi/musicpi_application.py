import logging
import subprocess
from enum import Enum
from pathlib import Path
from time import sleep

from PIL import Image, ImageDraw, ImageFont
from super_state_machine import machines

from musicpi import Mpd, SongInfo, Status
from musicpi.hmi.hmi import Hmi

LOG = logging.getLogger(__name__)

icon_pause = Image.open(Path("musicpi/hmi/icons/pause.png"))
icon_play = Image.open(Path("musicpi/hmi/icons/play.png"))
icon_repeat = Image.open(Path("musicpi/hmi/icons/repeat.png"))
icon_no_repeat = Image.open(Path("musicpi/hmi/icons/no_repeat.png"))
icon_random = Image.open(Path("musicpi/hmi/icons/random.png"))
icon_no_random = Image.open(Path("musicpi/hmi/icons/no_random.png"))


def mount_multimedia_if_necessary():
    if not Path("/home/max/Multimedia").is_mount():
        try:
            subprocess.call(["mount", "/home/max/Multimedia"], timeout=10)
        except subprocess.TimeoutExpired:
            LOG.error("couldn't mount Multimedia within 10s")


class MusicPi:
    def __init__(self, hmi: Hmi, cfg: dict) -> None:
        self._hmi = hmi
        self._cfg = cfg
        self._mpd = Mpd(cfg.get("mpd", {}))

    def start(self) -> None:
        menu = Menu()
        while True:
            if menu.state == "songinfo":
                self.visualize_current_song()
            if self._hmi.button.pressed():
                self._mpd.pause_play()
            self.set_led_to_playstatus()
            mount_multimedia_if_necessary()
            sleep(0.1)

    def set_led_to_playstatus(self) -> None:
        if self._mpd.status().playing:
            self._hmi.led.on()
        else:
            self._hmi.led.off()

    def visualize_current_song(self) -> None:
        song_info: SongInfo = self._mpd.current_song()
        status: Status = self._mpd.status()
        fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
        display_content = Image.new(mode="1", size=(128, 64), color=0)
        canvas = ImageDraw.Draw(display_content)
        visualisation = SongVisualisation(display_content, status, song_info)
        visualisation.display_status()
        if song_info.title:
            ...
        else:
            canvas.text((0, 0), "empty playlist", fill="white", font=fnt)
        self._hmi.show_on_display(display_content)


class SongVisualisation:
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
        self._display_playlist_position()

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
        try:
            pos_string = f"({self._song_info.id}/{self._status.playlistlength})"
        except KeyError:
            pos_string = "(N/A)"
        self._canvas.text((48, 48), text=pos_string, fill="white", font=self._font)


class Menu(machines.StateMachine):
    class States(Enum):
        SONGINFO = "songinfo"
        MAIN_MENU = "main_menu"
        CMD_NEXTSONG = "cmd_nextsong"
        SUBMENU_SYS_STATS = "submenu_sys_stats"
        SUBMENU_BT_STATS = "submenu_bt_stats"
        CMD_UPDATE_DB = "cmd_update_db"
        CMD_SHUTDOWN = "cmd_shutdown"

    class Meta:
        initial_state = "songinfo"
        transitions = {
            "songinfo": ["main_menu"],
            "main_menu": ["cmd_nextsong", "submenu_sys_stats", "submenu_bt_stats", "cmd_update_db", "cmd_shutdown"],
            "cmd_nextsong": ["main_menu"],
            "submenu_sys_stats": ["songinfo"],
            "submenu_bt_stats": ["songinfo"],
            "cmd_update_db": ["songinfo"],
        }
        named_transisitions = [
            ("open_main_menu", "main_menu", ["songinfo"]),
            ("open_submenu_sys_stats", "submenu_sys_stats"),
            ("open_submenu_bt_stats", "submenu_bt_stats"),
            ("close_menu", "songinfo"),
            ("call_cmd_nextsong", "cmd_nextsong"),
            ("call_cmd_update_db", "cmd_update_db"),
            ("call_cmd_shutdown", "cmd_shutdown"),
        ]
