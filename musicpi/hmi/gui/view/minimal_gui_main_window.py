
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QWidget

from resources import resources_rc  # needs to be here for self._load_ui(":/ui/main_window.ui") to work


class MinimalGUIMainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self._ui = self._load_ui(":/ui/minimal_main_window.ui")
        self._init_gui()

    def _load_ui(self, resource_path: str) -> QWidget:
        loader = QUiLoader(self)
        file = QFile(resource_path)
        if file.open(QFile.ReadOnly):
            ui = loader.load(file)
            file.close()
            self.setCentralWidget(ui)
            return ui
        else:
            raise FileNotFoundError(f"{resource_path} not found")

    def _init_gui(self) -> None:
        self.setWindowTitle(self._ui.windowTitle())
        self.resize(self._ui.size())
        self.setWindowIcon(self._ui.windowIcon())