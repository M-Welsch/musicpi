import sys

from PIL import Image, ImageDraw
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QApplication
from signalslot import Signal

from musicpi.hmi.gui.view.mockup_gui_window import MockupGuiWindow
from musicpi.hmi.hmi import Hmi


class Button:
    @staticmethod
    def pressed() -> bool:
        return False


class Led:
    @staticmethod
    def on() -> None:
        ...

    @staticmethod
    def off() -> None:
        ...


class HmiX86X64(Hmi):
    update_display = Signal(args=["image"])

    def __init__(self) -> None:
        ...

    def start(self) -> None:
        QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        app = MockupGui()
        sys.exit(app.exec())

    def show_on_display(self, image: Image) -> None:
        self.update_display.emit(image=image)

    @property
    def button(self) -> Button:
        return Button()

    @property
    def led(self) -> Led:
        return Led()


class MockupGui(QApplication):
    def __init__(self) -> None:
        super().__init__()
        self._main_window: MockupGuiWindow = MockupGuiWindow()
        self._main_window.show()
