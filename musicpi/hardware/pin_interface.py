from __future__ import annotations

from platform import machine
from time import sleep, time
from typing import Any, Optional

from signalslot import Signal

if not machine() in ["armv6l", "armv7l"]:
    print("Not on Single Board Computer. Importing Mockup for RPi.GPIO")
    import sys
    from importlib import import_module

    sys.modules["RPi"] = import_module("test.mockups.RPi_mock")

import logging
from pathlib import Path

import RPi.GPIO as GPIO

from musicpi.hardware.buttons import Buttons

LOG = logging.getLogger(Path(__file__).name)


class Pins:
    enc = {"a": 27, "b": 17}  # Pin 13  # Pin 11
    buttons = {"enc_sw": 22, "button": 4}  # Pin 15  # Pin 7
    leds = {"green": 23}  # pin 16


class PinInterface:
    __instance: Optional[PinInterface] = None

    @staticmethod
    def global_instance() -> PinInterface:
        """Static access method."""
        if PinInterface.__instance is None:
            PinInterface()
        assert isinstance(PinInterface.__instance, PinInterface)
        return PinInterface.__instance

    def __init__(self) -> None:
        """Virtually private constructor."""
        if PinInterface.__instance is not None:
            raise RuntimeError("This class is a singleton. Use global_instance() instead!")
        PinInterface.__instance = self
        GPIO.setmode(GPIO.BCM)

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


class Encoder(object):
    val_changed = Signal()
    """
    Encoder class allows to work with rotary encoder
    which connected via two pin A and B.
    Works only on interrupts because all RPi pins allow that.
    This library is a simple port of the Arduino Encoder library
    (https://github.com/PaulStoffregen/Encoder)
    
    Edit Maxi Welsch:
    - add signal
    """

    def __init__(self) -> None:
        self._pin_interface = PinInterface.global_instance()
        self.A = Pins.enc["a"]
        self.B = Pins.enc["b"]
        self._setup_encoder_pins()
        self.pos = 0
        self.state = 0
        if GPIO.input(self.A):
            self.state |= 1
        if GPIO.input(self.B):
            self.state |= 2
        self._pos_old = 0

    def _setup_encoder_pins(self) -> None:
        for enc_pin in Pins.enc.values():
            GPIO.setup(enc_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.A, GPIO.BOTH, callback=self.__update)
        GPIO.add_event_detect(self.B, GPIO.BOTH, callback=self.__update)

    """
    update() calling every time when value on A or B pins changes.
    It updates the current position based on previous and current states
    of the rotary encoder.
    """

    def __update(self, channel: Any) -> None:
        state = self.state & 3
        if GPIO.input(self.A):
            state |= 4
        if GPIO.input(self.B):
            state |= 8

        self.state = state >> 2

        if state == 1 or state == 7 or state == 8 or state == 14:
            self.pos += 1
        elif state == 2 or state == 4 or state == 11 or state == 13:
            self.pos -= 1
        elif state == 3 or state == 12:
            self.pos += 2
        elif state == 6 or state == 9:
            self.pos -= 2

        if not self.pos == self._pos_old:
            self.val_changed.emit()
            self._pos_old = self.pos

    """
    read() simply returns the current position of the rotary encoder.
    """

    def read(self) -> int:
        return self.pos


class Button:
    sig_pressed = Signal(args=["button"])
    last_press: float = 0

    def __init__(self) -> None:
        self._pin_interface = PinInterface.global_instance()
        self._setup_pins()

    def _setup_pins(self) -> None:
        for button in Pins.buttons.values():
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(Pins.buttons["button"], GPIO.FALLING, callback=self.on_pressed)
        GPIO.add_event_detect(
            Pins.buttons["enc_sw"],
            GPIO.FALLING,
            callback=lambda _: self.sig_pressed.emit(button=Buttons.ENCODER_BUTTON),
        )

    def on_pressed(self) -> None:
        if self.last_press - time() > 0.2:
            self.sig_pressed.emit(button=Buttons.PUSHPUTTON)
            self.last_press = time()

    def pressed(self) -> bool:
        return self._pin_interface.button_pressed()


class Led:
    def __init__(self) -> None:
        self._pin_interface = PinInterface.global_instance()
        self._setup_leds()

    @staticmethod
    def _setup_leds() -> None:
        for led_pin in Pins.leds.values():
            GPIO.setup(led_pin, GPIO.OUT)

    def on(self) -> None:
        self._pin_interface.led_on()

    def off(self) -> None:
        self._pin_interface.led_off()

    def state(self) -> bool:
        return self._pin_interface.led_state()
