import threading
import time

import keyboard
import pyperclip
import pytesseract
from PIL import ImageGrab

from overlay.mcq.config import (
    ANSWER_POPUP_MS,
    LETTER_HOTKEY,
    POPUP_MS,
    REGION_BBOX,
    SCREENSHOT_HOTKEY,
    SHOW_HOTKEY,
)
from overlay.mcq.gemini import get_answer
from overlay.mcq.toast import schedule_toast

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

last_answer = "No answer yet"
counter = 0


def save_string(text: str) -> None:
    with open("record_mcq.txt", "a") as file:
        file.write(text + "\n\n\n")


def _safe_paste():
    try:
        return pyperclip.paste() or ""
    except Exception as e:
        print("[ERROR] pyperclip.paste failed:", e)
        return ""


def _wait_clipboard_new_content(prev_text: str, timeout=1.0):
    print("[DEBUG] Waiting for clipboard to update...")
    t0 = time.time()
    while time.time() - t0 < timeout:
        cur = _safe_paste()
        if cur.strip() and cur != (prev_text or ""):
            print("[DEBUG] Detected new clipboard content.")
            return cur
        time.sleep(0.05)
    print("[WARN] Clipboard did not change within timeout.")
    return ""


def capture_ocr_text(bbox=REGION_BBOX) -> str:
    try:
        time.sleep(0.5)
        img = ImageGrab.grab(bbox=bbox)
        text = pytesseract.image_to_string(img)
        return (text or "").strip()
    except Exception as e:
        print("[ERROR] Screenshot/OCR failed:", e)
        return ""


def _solve_and_store(bridge, question_text: str, show_immediately: bool = False):
    global last_answer, counter

    ans = get_answer(question_text)
    last_answer = ans
    counter += 1
    save_string(last_answer)
    print("[INFO] Saved last answer:", last_answer)
    if show_immediately:
        schedule_toast(bridge, last_answer, POPUP_MS)


def on_detected_copy_combo(bridge):
    prev = _safe_paste()
    time.sleep(0.12)
    clip = _wait_clipboard_new_content(prev, timeout=1.0) or _safe_paste()

    if not clip.strip():
        print("[WARN] Clipboard empty or unchanged after copy.")
        schedule_toast(bridge, "Clipboard empty")
        return

    print("[INFO] Clipboard captured (first 120 chars):")
    print(clip[:120] + ("..." if len(clip) > 120 else ""))
    save_string(clip)

    threading.Thread(
        target=lambda: _solve_and_store(bridge, clip),
        daemon=True,
    ).start()


def on_screenshot_hotkey(bridge):
    print("[INFO] 'm' pressed — starting OCR capture...")

    def worker():
        question_text = capture_ocr_text(REGION_BBOX)
        if not question_text:
            print("[WARN] No OCR text captured.")
            schedule_toast(bridge, "No text found", 300)
            return
        print("[INFO] OCR text (first 120 chars):")
        print(question_text[:120] + ("..." if len(question_text) > 120 else ""))
        save_string(question_text)
        _solve_and_store(bridge, question_text, show_immediately=True)

    threading.Thread(target=worker, daemon=True).start()


def on_show_hotkey(bridge):
    print("[INFO] Show hotkey pressed. Displaying last answer.")
    schedule_toast(bridge, f"{last_answer} ({counter})", ANSWER_POPUP_MS)


def on_letter_release(bridge, event=None):
    print("[INFO] 'l' key released -> showing last answer.")
    schedule_toast(bridge, f"{last_answer} ({counter})", ANSWER_POPUP_MS)


def register_hotkeys(bridge):
    keyboard.on_release_key(
        SCREENSHOT_HOTKEY,
        lambda e: on_screenshot_hotkey(bridge),
        suppress=False,
    )
    keyboard.on_release_key(
        LETTER_HOTKEY,
        lambda e: on_letter_release(bridge),
        suppress=False,
    )
    keyboard.add_hotkey(SHOW_HOTKEY, lambda: on_show_hotkey(bridge), suppress=False)
