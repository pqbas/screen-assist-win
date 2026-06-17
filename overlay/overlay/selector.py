from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication


class CaptureManager(QObject):
    capture_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.capture_requested.connect(self._do_capture)

    def request_capture(self):
        self.capture_requested.emit()

    def _do_capture(self):
        try:
            screen = QApplication.primaryScreen()
            pixmap = screen.grabWindow(0)
            QApplication.clipboard().setPixmap(pixmap)
            print("[INFO] Full screen captured to clipboard")
        except Exception as e:
            print(f"[ERROR] Screenshot failed: {e}")
