import json
import subprocess
from pathlib import Path

import keyboard

from overlay.overlay.selector import capture_fullscreen
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
        self._switch_hotkey = keyboard.add_hotkey("alt+shift", self.switch_app, suppress=True)
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
        for hk in (self._toggle_hotkey, self._switch_hotkey, self._capture_hotkey, self._vscode_hotkey):
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

    def switch_app(self):
        hwnd = self._find_window("Visual Studio Code")
        if hwnd is None:
            print("[WARN] VSCode window not found")
            return

        import win32con
        import win32gui

        foreground = win32gui.GetForegroundWindow()
        if hwnd == foreground:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            print("[INFO] VSCode minimized")
        else:
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            print("[INFO] VSCode restored")

    def _find_window(self, title_part: str):
        import win32gui

        results = []

        def enum_cb(hwnd, _results):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title and title_part.lower() in title.lower():
                    _results.append(hwnd)
            return True

        win32gui.EnumWindows(enum_cb, results)
        return results[0] if results else None

    def capture_to_clipboard(self):
        capture_fullscreen()

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
