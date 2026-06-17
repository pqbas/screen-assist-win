from io import BytesIO

import win32clipboard
from PIL import ImageGrab


def capture_fullscreen():
    try:
        img = ImageGrab.grab()
        output = BytesIO()
        img.convert("RGB").save(output, format="BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        print("[INFO] Full screen captured to clipboard")
    except Exception as e:
        print(f"[ERROR] Screenshot failed: {e}")
