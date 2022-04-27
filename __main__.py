import logging
from datetime import datetime
from pathlib import Path
from platform import machine

import yaml

from musicpi.hmi.hmi import Hmi
from musicpi.musicpi_application import MusicPi

LOG = logging.getLogger(__name__)


def setup_logger(cfg_log: dict) -> None:
    log_path = Path(cfg_log["path"])
    log_path.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=log_path / datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log"),
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s: %(name)s: %(message)s",
        datefmt="%m.%d.%Y %H:%M:%S",
    )


if __name__ == "__main__":
    with open("config.yml", "r") as cf:
        cfg = yaml.safe_load(cf)
    setup_logger(cfg["log"])

    if machine() in ["armv6l", "armv7l"]:
        print("Raspi")
        from musicpi.hmi.hmi_arm import HmiArm

        h: Hmi = HmiArm()
    elif machine() == "x86_64":
        print("Laptop")
        from musicpi.hmi.hmi_x86_64 import HmiX86X64

        h: Hmi = HmiX86X64()  # type: ignore
    else:
        raise ValueError("I don't know who I am! Problably the hardware platform is not supported (yet)!")
    MusicPi(hmi=h, cfg=cfg.get("logic", {}))
