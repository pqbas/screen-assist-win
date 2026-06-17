import win32clipboard
from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt6.QtWidgets import QWidget, QApplication


class RegionSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setCursor(Qt.CursorShape.CrossCursor)

        screen = QApplication.primaryScreen()
        self.setGeometry(screen.geometry())

        self._origin: QPoint | None = None
        self._current: QPoint | None = None
        self._selection = QRect()

        self.showFullScreen()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        overlay = QColor(0, 0, 0, 80)
        painter.fillRect(self.rect(), overlay)

        if not self._selection.isNull():
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(self._selection, Qt.GlobalColor.transparent)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)

            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)
            painter.drawRect(self._selection)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._origin = event.position().toPoint()
            self._current = self._origin
            self._selection = QRect(self._origin, self._current)

    def mouseMoveEvent(self, event):
        if self._origin:
            self._current = event.position().toPoint()
            self._selection = QRect(self._origin, self._current).normalized()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self._selection.isNull():
            self.hide()
            QApplication.processEvents()
            self._capture_region(self._selection)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def _capture_region(self, rect: QRect):
        screen = QApplication.primaryScreen()
        pixmap = screen.grab(rect.x(), rect.y(), rect.width(), rect.height())
        image = pixmap.toImage()

        width = image.width()
        height = image.height()

        bmp_header_size = 14
        dib_header_size = 40
        row_size = ((width * 24 + 31) // 32) * 4
        pixel_data_size = row_size * height
        file_size = bmp_header_size + dib_header_size + pixel_data_size

        data = bytearray()
        # BMP header
        data.extend(b'BM')
        data.extend(file_size.to_bytes(4, 'little'))
        data.extend(b'\x00\x00\x00\x00')
        data.extend((bmp_header_size + dib_header_size).to_bytes(4, 'little'))
        # DIB header
        data.extend(dib_header_size.to_bytes(4, 'little'))
        data.extend(width.to_bytes(4, 'little'))
        data.extend(height.to_bytes(4, 'little'))
        data.extend((1).to_bytes(2, 'little'))
        data.extend((24).to_bytes(2, 'little'))
        data.extend(b'\x00\x00\x00\x00')
        data.extend(pixel_data_size.to_bytes(4, 'little'))
        data.extend(b'\x00\x00\x00\x00')
        data.extend(b'\x00\x00\x00\x00')
        data.extend(b'\x00\x00\x00\x00')
        data.extend(b'\x00\x00\x00\x00')

        # Pixel data (bottom-up, BGR)
        for y in range(height - 1, -1, -1):
            for x in range(width):
                px = image.pixelColor(x, y)
                data.extend([
                    px.blue(),
                    px.green(),
                    px.red(),
                ])
            padding = row_size - width * 3
            data.extend(b'\x00' * padding)

        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bytes(data))
            win32clipboard.CloseClipboard()
            print("[INFO] Region captured to clipboard")
        except Exception as e:
            print(f"[ERROR] Clipboard failed: {e}")

        self.close()
