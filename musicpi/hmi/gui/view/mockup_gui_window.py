from PIL import Image
from PySide6 import QtWidgets
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QCheckBox, QGraphicsView, QMainWindow, QPushButton, QWidget
from signalslot import Signal

from musicpi.hardware.buttons import Buttons
from musicpi.hmi.gui.resources import resources_rc  # needs to be here for self._load_ui(":/ui/main_window.ui") to work


class MockupGuiWindow(QMainWindow):
    sig_pressed = Signal(args=["button"])
    val_changed = Signal(args=["amount"])

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

    def update_display(self, image, *args, **kwargs):  # type: ignore
        print("show")
        image: Image.Image
        pix = image.toqpixmap()
        item = QtWidgets.QGraphicsPixmapItem(pix)
        scene = QtWidgets.QGraphicsScene(self)
        scene.addItem(item)
        self.gV_display.setScene(scene)

    def slot_pb_cw_clicked(self) -> None:
        self.val_changed.emit(amount=1)

    def slot_pb_ccw_clicked(self) -> None:
        self.val_changed.emit(amount=-1)

    def slot_pb_push_clicked(self) -> None:
        self.sig_pressed.emit(button=Buttons.ENCODER_BUTTON)

    def slot_pb_button_clicked(self) -> None:
        self.sig_pressed.emit(button=Buttons.PUSHPUTTON)
