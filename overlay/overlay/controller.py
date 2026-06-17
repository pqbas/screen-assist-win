import json
import subprocess
from io import BytesIO
from pathlib import Path

import keyboard
import win32clipboard
from PIL import ImageGrab

from overlay.overlay.window import OverlayImage, TaskbarOverlay, native_image_size
from overlay.utils import assets_dir


class OverlayController:
    def __init__(self, app):
        self.app = app
        self.visible = True
        screen = app.primaryScreen()
        screen_rect = screen.geometry()
        base = assets_dir()

        self._vscode_folder = self._load_vscode_folder()

        self.block_windows_key()

        taskbar_path = str(base / "taskbar.png")
        close_button_path = str(base / "close_button.png")

        self.taskbar_overlay = TaskbarOverlay(
            taskbar_path,
            screen_rect.width(),
            screen_rect.height(),
        )

        close_w, _ = native_image_size(close_button_path)
        self.close_button_overlay = OverlayImage(
            close_button_path,
            screen_rect.width() - close_w,
            0,
        )

        self._toggle_hotkey = keyboard.add_hotkey("ctrl+alt+t", self.toggle_visibility)
        self._capture_hotkey = keyboard.add_hotkey("ctrl+shift+s", self.capture_to_clipboard)
        self._vscode_hotkey = keyboard.add_hotkey("ctrl+alt+v", self.open_vscode)

    def block_windows_key(self):
        try:
            keyboard.block_key("left windows")
            keyboard.block_key("right windows")
            print("Windows key disabled")
        except Exception as e:
            print(f"Error blocking Windows key: {e}")

    def unblock_windows_key(self):
        try:
            keyboard.unblock_key("left windows")
            keyboard.unblock_key("right windows")
            print("Windows key enabled")
        except Exception as e:
            print(f"Error unblocking Windows key: {e}")

    def shutdown(self):
        print("Closing overlay...")
        for hk in (self._toggle_hotkey, self._capture_hotkey, self._vscode_hotkey):
            try:
                keyboard.remove_hotkey(hk)
            except Exception:
                pass
        self.unblock_windows_key()
        for widget in (self.taskbar_overlay, self.close_button_overlay):
            widget.close()

    def toggle_visibility(self):
        self.visible = not self.visible
        if self.visible:
            self.taskbar_overlay.show()
            self.close_button_overlay.show()
            self.block_windows_key()
        else:
            self.taskbar_overlay.hide()
            self.close_button_overlay.hide()
            self.unblock_windows_key()

    def capture_to_clipboard(self):
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
            print("[INFO] Screenshot copied to clipboard")
        except Exception as e:
            print(f"[ERROR] Screenshot failed: {e}")

    def open_vscode(self):
        try:
            folder = self._vscode_folder
            if folder:
                subprocess.Popen(["code", folder], shell=True)
                print(f"[INFO] Launching VSCode in {folder}")
            else:
                subprocess.Popen(["code"], shell=True)
                print("[INFO] Launching VSCode (no folder configured)")
        except Exception as e:
            print(f"[ERROR] Failed to open VSCode: {e}")

    def _load_vscode_folder(self) -> str | None:
        config_path = Path(__file__).resolve().parent.parent / "config.json"
        if not config_path.exists():
            return None
        try:
            with open(config_path) as f:
                cfg = json.load(f)
            folder = cfg.get("vscode_folder", "").strip()
            return folder if folder else None
        except Exception:
            return None


def run(app) -> OverlayController:
    return OverlayController(app)
