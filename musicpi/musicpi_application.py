from time import sleep

from luma.core.render import canvas
from PIL import Image, ImageDraw, ImageFont

from musicpi import Mpd
from musicpi.hmi.hmi import Hmi


class MusicPi:
    def __init__(self, hmi: Hmi, cfg: dict) -> None:
        self._hmi = hmi
        self._cfg = cfg
        self._mpd = Mpd(cfg.get("mpd", {}))

    def visualize_current_song(self) -> None:
        fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
        display_content = Image.new(mode="1", size=(128, 64), color=0)
        canvas = ImageDraw.Draw(display_content)
        posy = 0
        canvas.text((5, posy), "Bluebber", fill="white", font=fnt)
        posy += 11
        self._hmi.show_on_display(display_content)
