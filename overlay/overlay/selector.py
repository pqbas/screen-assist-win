from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor
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

        self._origin = None
        self._current = None
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
        QApplication.clipboard().setPixmap(pixmap)
        print("[INFO] Region captured to clipboard")
        self.close()
