from enum import Enum
from pathlib import Path
from time import sleep
from typing import Callable

from PIL import Image, ImageDraw, ImageFont
from signalslot import Signal
from super_state_machine import machines

from musicpi import Mpd, SongInfo, Status
from musicpi.hardware.buttons import Buttons
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
        self._menu_visualisation = MenuVisualisation(menu_leave_hook=self._connect_signals_to_song_visualisation)
        self._connect_common_signals()
        self._connect_signals_to_song_visualisation()
        self._hmi.start()

    def _connect_common_signals(self) -> None:
        self._hmi.trigger_repeated_event.connect(self.visualize_display_content)

    def _connect_signals_to_song_visualisation(self) -> None:
        self._hmi.button_pressed.disconnect(self._menu_visualisation.on_button_pressed)
        self._hmi.button_pressed.connect(self.on_button_pressed)
        self._hmi.encoder_value_changed.disconnect(self._menu_visualisation.encoder_value_changed)
        self._hmi.encoder_value_changed.connect(self.encoder_value_changed)

    def _connect_signals_to_menu_visualisation(self) -> None:
        self._hmi.button_pressed.disconnect(self.on_button_pressed)
        self._hmi.button_pressed.connect(self._menu_visualisation.on_button_pressed)
        self._hmi.encoder_value_changed.disconnect(self.encoder_value_changed)
        self._hmi.encoder_value_changed.connect(self._menu_visualisation.encoder_value_changed)

    def on_button_pressed(self, button, *args, **kwargs):  # type: ignore
        button: Buttons
        print(f"button pressed {button.value}")
        if button == Buttons.PUSHPUTTON:
            self._mpd.pause_play()
        if button == Buttons.ENCODER_BUTTON:
            self._menu_visualisation.enter_menu()
            self._connect_signals_to_menu_visualisation()

    def encoder_value_changed(self, amount, *args, **kwargs):  # type: ignore
        print(f"enc val changed by {amount}")

    def set_led_to_playstatus(self) -> None:
        if self._mpd.status().playing:
            self._hmi.led.on()
        else:
            self._hmi.led.off()

    def visualize_display_content(self, *args, **kwargs):  # type: ignore
        if self._menu_visualisation:
            self.visualize_menu()
        else:
            self.visualize_current_song()
        self.set_led_to_playstatus()

    def visualize_menu(self) -> None:
        print("bi")
        self._hmi.show_on_display(self._menu_visualisation.display_content)

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


class MenuVisualisation:
    def __init__(self, menu_leave_hook: Callable) -> None:
        self._menu = Menu()
        self._menu_leave_hook = menu_leave_hook
        self._fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
        self._display_content = Image.new(mode="1", size=(128, 64), color=0)

    def on_button_pressed(self, button, *args, **kwargs):  # type: ignore
        if button == Buttons.PUSHPUTTON and self._menu.state == "main_menu":
            self.exit_menu()

    def enter_menu(self) -> None:
        self._menu.set_main_menu()
        canvas = ImageDraw.Draw(self._display_content)
        canvas.text((0, 0), "Skip Song", fill="white", font=self._fnt)

    def exit_menu(self) -> None:
        self._menu_leave_hook()  # map disconnect signals
        # show song info again

    def encoder_value_changed(self, amount, *args, **kwargs):  # type: ignore
        ...

    @property
    def display_content(self) -> Image:
        return self._display_content

    @property
    def active(self) -> bool:
        return not self._menu.state == "song_info"


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
