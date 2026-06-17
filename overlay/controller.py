import sys

from PyQt6.QtWidgets import QApplication

import overlay.overlay.controller
from overlay.utils import release_keyboard_hooks, setup_signal_handling


def run():
    app = QApplication(sys.argv)
    overlay_ctrl = overlay.overlay.controller.run(app)
    shutdown_state = {"done": False}

    def shutdown():
        if shutdown_state["done"]:
            return
        shutdown_state["done"] = True

        overlay_ctrl.shutdown()
        release_keyboard_hooks()

    app.aboutToQuit.connect(shutdown)
    setup_signal_handling(app, on_interrupt=shutdown)

    exit_code = app.exec()
    shutdown()
    sys.exit(exit_code)
