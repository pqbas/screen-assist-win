import pyautogui

GEMINI_DEFAULT_MODEL = "gemini-2.0-flash"

SHOW_HOTKEY = "f8"
LETTER_HOTKEY = "l"
SCREENSHOT_HOTKEY = "m"
POPUP_MS = 500
ANSWER_POPUP_MS = 500
MARGIN_PX = 14
FONT_FAMILY = "Segoe UI"
FONT_SIZE = 8

REGION_BBOX = (0, 0, pyautogui.size()[0], pyautogui.size()[1])

PROMPT_TEMPLATE = """You are given a multiple-choice question copied by the user.
Reply with a SINGLE concise correct option LETTER, or the ANSWER TEXT IF THE LETTER IS NOT GIVEN.
No explanations. Example: "B"

Question:
{question}
"""
