import signal
from pathlib import Path

from PyQt6.QtCore import QTimer


def assets_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "assets"


def release_keyboard_hooks() -> None:
    try:
        import keyboard

        keyboard.unhook_all()
    except Exception:
        pass


def setup_signal_handling(app, on_interrupt=None) -> QTimer:
    """Allow Ctrl+C in the terminal to quit on Windows (keyboard hooks block SIGINT otherwise)."""

    def handler(signum, frame):
        print("\nCtrl+C received — shutting down...")
        release_keyboard_hooks()
        if on_interrupt:
            on_interrupt()
        app.quit()

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)
    return timer
