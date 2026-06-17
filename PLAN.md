# Plan: Reemplazar OCR/Gemini por captura de pantalla + lanzar VSCode

## Objetivo

Eliminar el modulo `mcq/` (OCR + Gemini) y agregar dos hotkeys nuevos:
- `Ctrl+Shift+S` → capturar pantalla completa al portapapeles (como imagen BMP)
- `Ctrl+Alt+V` → abrir VSCode

## Archivos a modificar

### 1. `overlay/controller.py`

Eliminar:
- `import overlay.mcq.controller`
- `mcq_bridge = overlay.mcq.controller.run(app)`
- `mcq_bridge.window.close()` del shutdown

### 2. `overlay/overlay/controller.py`

Agregar imports:
```python
import subprocess
import win32clipboard
from io import BytesIO
from PIL import ImageGrab
```

Agregar metodos a `OverlayController`:
```python
def capture_to_clipboard(self):
    img = ImageGrab.grab()
    output = BytesIO()
    img.convert("RGB").save(output, format="BMP")
    data = output.getvalue()[14:]
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def open_vscode(self):
    subprocess.Popen(["code"], shell=True)
```

Registrar hotkeys en `__init__`:
```python
keyboard.add_hotkey("ctrl+shift+s", self.capture_to_clipboard)
keyboard.add_hotkey("ctrl+alt+v", self.open_vscode)
```

## Resultado final

| Tecla            | Accion                            |
|------------------|-----------------------------------|
| `Ctrl+Shift+S`   | Captura pantalla -> portapapeles   |
| `Ctrl+Alt+V`     | Abre VSCode                       |
| `Ctrl+Alt+T`     | Oculta/muestra overlay (existente) |

Se eliminan las teclas `M`, `L` y `F8` (eran del modulo `mcq/`).
