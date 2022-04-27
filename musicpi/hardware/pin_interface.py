from __future__ import annotations

from platform import machine
from time import sleep
from typing import Optional

if not machine() in ["armv6l", "armv7l"]:
    print("Not on Single Board Computer. Importing Mockup for RPi.GPIO")
    import sys
    from importlib import import_module

    sys.modules["RPi"] = import_module("test.mockups.RPi_mock")

from Encoder import Encoder
import RPi.GPIO as GPIO


import logging
from pathlib import Path

LOG = logging.getLogger(Path(__file__).name)


class Pins:
    enc = {"a": 27, "b": 17}  # Pin 13  # Pin 11
    buttons = {"enc_sw": 22, "button": 4}  # Pin 15  # Pin 7
    leds = {"green": 23}  # pin 16


class PinInterface:
    __instance: Optional[PinInterface] = None

    @staticmethod
    def global_instance() -> PinInterface:
        """ Static access method. """
        if PinInterface.__instance is None:
            PinInterface()
        return PinInterface.__instance

    def __init__(self) -> None:
        """ Virtually private constructor. """
        if PinInterface.__instance is not None:
            raise RuntimeError("This class is a singleton. Use global_instance() instead!")
        PinInterface.__instance = self
        self._encoder = Encoder(Pins.enc["a"], Pins.enc["b"])
        self._setup_encoder_pins()
        # GPIO init happens in Encoder(...)
        self._setup_buttons()
        self._setup_leds()

    @staticmethod
    def _setup_buttons() -> None:
        for button in Pins.buttons.values():
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(button, GPIO.FALLING)

    @staticmethod
    def _setup_encoder_pins() -> None:
        for enc_pin in Pins.enc.values():
            GPIO.setup(enc_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    @staticmethod
    def _setup_leds() -> None:
        for led_pin in Pins.leds.values():
            GPIO.setup(led_pin, GPIO.OUT)

    def encoder_value(self) -> int:
        return self._encoder.read()

    def button_pressed(self) -> bool:
        return not bool(GPIO.input(Pins.buttons["button"]))

    def encoder_sw_pressed(self) -> bool:
        return not bool(GPIO.input(Pins.buttons["enc_sw"]))

    def led_on(self) -> None:
        GPIO.output(Pins.leds["green"], GPIO.HIGH)

    def led_off(self) -> None:
        GPIO.output(Pins.leds["green"], GPIO.LOW)

    def led_state(self) -> bool:
        return bool(GPIO.input(Pins.leds["green"]))

    def cleanup(self) -> None:
        GPIO.cleanup()


class RotaryEncoder:
    def __init__(self) -> None:
        self._pin_interface = PinInterface.global_instance()

    def read(self) -> int:
        return self._pin_interface.encoder_value()


class Button:
    def __init__(self) -> None:
        self._pin_interface = PinInterface.global_instance()

    def pressed(self) -> bool:
        return self._pin_interface.button_pressed()


class Led:
    def __init__(self) -> None:
        self._pin_interface = PinInterface.global_instance()

    def on(self) -> None:
        self._pin_interface.led_on()

    def off(self) -> None:
        self._pin_interface.led_off()

    def state(self) -> bool:
        return self._pin_interface.led_state()
