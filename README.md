## Screen Assist for Windows

Windows overlay tool that sits on top of your screen and provides quick shortcuts for taking screenshots and launching VSCode.

---

## Features

| Shortcut | Action |
|----------|--------|
| `Ctrl+Alt+T` | Toggle overlay visibility / Win key lock |
| `Ctrl+Shift+S` | Capture full screen to clipboard |
| `Ctrl+Alt+V` | Launch VSCode |

The Win key is automatically blocked while the overlay is visible, and unblocked when hidden.

---

## Prerequisites

- Python 3.11+
- Windows (uses win32 APIs)
- VSCode installed and `code` command available in PATH

---

## Setup

```bash
git clone https://github.com/pqbas/screen-assist-win
cd screen-assist-win
pip install -r requirements.txt
python -m setup
python -m overlay
```

After the overlay starts, press `Ctrl+Alt+T` to hide/show it. Screenshots go to your clipboard — just `Ctrl+V` to paste anywhere.

---

## Project structure

```
setup/          Downloads and installs compatible SEB version + patch
overlay/        Main overlay application
  overlay/      PyQt6 window layer + hotkey controller
  mcq/          OCR + Gemini solver (removed)
assets/         PNG images used by the overlay (taskbar, buttons)
```

---

## Disabling Windows shortcuts

For a cleaner experience, disable these in Windows Settings:

- `Ctrl+Win+Arrow` (switches desktop)
- Three/four finger swipe (opens Task View)

---

## Contributing

Pull requests welcome. Describe what you changed and why.
