from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QCheckBox, QGraphicsView, QMainWindow, QPushButton, QWidget

from musicpi.hmi.gui.resources import resources_rc  # needs to be here for self._load_ui(":/ui/main_window.ui") to work


class MockupGuiWindow(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self._ui = self._load_ui(":/ui/frontplate_conf.ui")
        self._init_gui()
        self.pb_cw = self.findChild(QPushButton, "pB_cw")
        self.pb_ccw = self.findChild(QPushButton, "pB_ccw")
        self.pb_push = self.findChild(QPushButton, "pB_push")
        self.pb_button = self.findChild(QPushButton, "pB_button")
        self.cB_led = self.findChild(QCheckBox, "cB_led")
        self.gV_display = self.findChild(QGraphicsView, "gV_display")

        self.pb_cw.clicked.connect(self.slot_pb_cw_clicked)
        self.pb_ccw.clicked.connect(self.slot_pb_ccw_clicked)
        self.pb_push.clicked.connect(self.slot_pb_push_clicked)
        self.pb_button.clicked.connect(self.slot_pb_button_clicked)

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

    def slot_pb_cw_clicked(self) -> None:
        print("cw clicked!")

    def slot_pb_ccw_clicked(self) -> None:
        ...

    def slot_pb_push_clicked(self) -> None:
        ...

    def slot_pb_button_clicked(self) -> None:
        ...
