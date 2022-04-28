import sys

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QApplication
from view.mockup_gui_window import MockupGuiWindow


class MinimalGui(QApplication):
    def __init__(self) -> None:
        super().__init__()
        self._main_window: MockupGuiWindow = MockupGuiWindow()
        self._main_window.show()


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = MinimalGui()
    sys.exit(app.exec())
