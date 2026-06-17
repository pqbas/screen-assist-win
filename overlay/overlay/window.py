from datetime import datetime

import win32con
import win32gui
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QWidget


def native_image_size(image_path: str) -> tuple[int, int]:
    """Logical Qt size so PNG pixels map 1:1 on screen (ignores Windows display scaling)."""

    pixmap = QPixmap(image_path)
    dpr = QApplication.primaryScreen().devicePixelRatio()
    return round(pixmap.width() / dpr), round(pixmap.height() / dpr)


def _load_native_pixmap(image_path: str) -> tuple[QPixmap, int, int]:
    pixmap = QPixmap(image_path)
    dpr = QApplication.primaryScreen().devicePixelRatio()
    pixmap.setDevicePixelRatio(dpr)
    width = round(pixmap.width() / dpr)
    height = round(pixmap.height() / dpr)
    return pixmap, width, height


class OverlayImage(QLabel):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        pixmap, width, height = _load_native_pixmap(image_path)
        self.setPixmap(pixmap)
        self.setFixedSize(width, height)
        self.move(x, y)

        self.show()
        self._configure_window()

    def _configure_window(self):
        hwnd = int(self.winId())

        win32gui.SetWindowLong(
            hwnd,
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED,
        )

        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE,
        )


class TaskbarOverlay(QWidget):
    """Stretch taskbar.png to full screen width; keep its native height. Shows live clock."""

    def __init__(self, image_path: str, screen_width: int, screen_height: int):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        _, height = native_image_size(image_path)
        width = screen_width
        dpr = QApplication.primaryScreen().devicePixelRatio()

        # Background image
        self._image = QLabel(self)
        pixmap = QPixmap(image_path).scaled(
            int(width * dpr),
            int(height * dpr),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        pixmap.setDevicePixelRatio(dpr)
        self._image.setPixmap(pixmap)
        self._image.setFixedSize(width, height)

        # Live clock
        self._clock = QLabel(self)
        self._clock.setFont(QFont("Segoe UI", 8, QFont.Weight.Normal))
        self._clock.setStyleSheet("color: #000000; background-color: rgb(240, 240, 240);")
        self._clock.setWordWrap(True)
        self._clock.adjustSize()

        clock_x = width - 160
        clock_y = height - 28
        self._clock.move(clock_x, clock_y)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_clock)
        self._timer.start(1000)
        self._update_clock()

        self.setFixedSize(width, height)
        self.move(0, screen_height - height)

        self.show()
        self._configure_window()

    def _update_clock(self):
        now = datetime.now()
        self._clock.setText(f"{now.strftime('%H:%M')}\n{now.strftime('%d/%m/%Y')}")
        self._clock.adjustSize()

    def _configure_window(self):
        hwnd = int(self.winId())

        win32gui.SetWindowLong(
            hwnd,
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED,
        )

        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE,
        )
