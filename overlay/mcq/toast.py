from PyQt6.QtCore import QObject, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

from overlay.mcq.config import FONT_FAMILY, FONT_SIZE, MARGIN_PX, POPUP_MS


class ToastWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.label = QLabel("", self)
        self.label.setFont(QFont(FONT_FAMILY, FONT_SIZE))
        self.label.setStyleSheet(
            "QLabel { color: #000000; background-color: rgb(240, 240, 240); "
            "padding: 1px 3px; border-radius: 6px; }"
        )

    def show_toast(self, text: str, duration_ms: int = POPUP_MS):
        print(f"[INFO] ToastWindow.show_toast: '{text}' ({duration_ms} ms)")
        single_line = text.replace("\n", " ").strip()
        self.label.setText(single_line)
        self.label.adjustSize()

        win_w = max(160, self.label.width())
        win_h = max(36, self.label.height())

        screen = QApplication.primaryScreen().geometry()
        x = screen.x() + screen.width() - win_w - int(MARGIN_PX * 2.2)
        y = screen.y() + screen.height() - win_h - int(MARGIN_PX / 2.2)

        self.setGeometry(int(x), int(y), win_w, win_h)
        self.label.move(0, 0)

        self.show()
        self.raise_()
        QTimer.singleShot(duration_ms, self.hide)


class ToastBridge(QObject):
    request_toast = pyqtSignal(str, int)

    def __init__(self, window: ToastWindow):
        super().__init__()
        self.window = window
        self.request_toast.connect(self._on_request)

    def _on_request(self, text: str, ms: int):
        self.window.show_toast(text, ms)


def build_toast(app):
    window = ToastWindow()
    bridge = ToastBridge(window)
    app._mcq_toast_window = window
    app._mcq_toast_bridge = bridge
    print("[INFO] PyQt6 toast UI built successfully.")
    return bridge


def schedule_toast(bridge, text: str, ms: int = POPUP_MS):
    if bridge is None:
        print(f"[TOAST] {text}")
        return
    bridge.request_toast.emit(text, ms)
