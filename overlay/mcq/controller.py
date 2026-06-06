from overlay.mcq.config import LETTER_HOTKEY, SCREENSHOT_HOTKEY, SHOW_HOTKEY
from overlay.mcq.handlers import register_hotkeys
from overlay.mcq.toast import build_toast, schedule_toast


def run(app):
    bridge = build_toast(app)
    register_hotkeys(bridge)

    print("===================================")
    print("MCQ Helper (Gemini) Running")
    print(f"OCR Screenshot: '{SCREENSHOT_HOTKEY}'")
    print(f"Show Answer: {SHOW_HOTKEY} or '{LETTER_HOTKEY}'")
    print("===================================")

    schedule_toast(
        bridge,
        f"MCQ helper active — OCR '{SCREENSHOT_HOTKEY}', show '{LETTER_HOTKEY}'",
        500,
    )

    return bridge
