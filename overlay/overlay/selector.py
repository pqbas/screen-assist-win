from PyQt6.QtWidgets import QApplication


def capture_fullscreen():
    try:
        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(0)
        QApplication.clipboard().setPixmap(pixmap)
        print("[INFO] Full screen captured to clipboard")
    except Exception as e:
        print(f"[ERROR] Screenshot failed: {e}")
