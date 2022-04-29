import sys
from typing import Callable

from PIL import Image, ImageDraw
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QApplication
from signalslot import Signal

from musicpi.hmi.gui.view.mockup_gui_window import MockupGuiWindow
from musicpi.hmi.hmi import Hmi


class Led:
    @staticmethod
    def on() -> None:
        ...

    @staticmethod
    def off() -> None:
        ...


class MockupGui(QApplication):
    def __init__(self) -> None:
        super().__init__()
        self._main_window: MockupGuiWindow = MockupGuiWindow()
        self._main_window.show()

    @property
    def on_update_display(self) -> Callable:
        return self._main_window.update_display  # type: ignore  # returning a slot

    @property
    def button_pressed(self) -> Signal:
        return self._main_window.sig_pressed

    @property
    def encoder_value_changed(self) -> Signal:
        return self._main_window.val_changed


class HmiX86X64(Hmi):
    update_display = Signal(args=["image"])

    def __init__(self) -> None:
        self._app = MockupGui()

    def connect_signals(self) -> None:
        self.update_display.connect(self._app.on_update_display)

    def start(self) -> None:
        QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        sys.exit(self._app.exec())

    def show_on_display(self, image: Image) -> None:
        self.update_display.emit(image=image)

    @property
    def button_pressed(self) -> Signal:
        return self._app.button_pressed

    @property
    def encoder_value_changed(self) -> Signal:
        return self._app.encoder_value_changed

    @property
    def led(self) -> Led:
        return Led()
