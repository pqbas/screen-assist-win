import keyboard

from overlay.overlay.window import OverlayImage, TaskbarOverlay, native_image_size
from overlay.utils import assets_dir


class OverlayController:
    def __init__(self, app):
        self.app = app
        self.visible = True
        screen = app.primaryScreen()
        screen_rect = screen.geometry()
        base = assets_dir()

        self.block_windows_key()

        reload_path = str(base / "reload.png")
        taskbar_path = str(base / "taskbar.png")
        close_button_path = str(base / "close_button.png")

        self.top_overlay = OverlayImage(reload_path, 0, 37)

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
        try:
            keyboard.remove_hotkey(self._toggle_hotkey)
        except Exception:
            pass
        self.unblock_windows_key()
        for widget in (self.top_overlay, self.taskbar_overlay, self.close_button_overlay):
            widget.close()

    def toggle_visibility(self):
        self.visible = not self.visible
        if self.visible:
            self.top_overlay.show()
            self.taskbar_overlay.show()
            self.close_button_overlay.show()
            self.block_windows_key()
        else:
            self.top_overlay.hide()
            self.taskbar_overlay.hide()
            self.close_button_overlay.hide()
            self.unblock_windows_key()


def run(app) -> OverlayController:
    return OverlayController(app)
