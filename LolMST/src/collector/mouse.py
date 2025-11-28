from pynput.mouse import Listener
import time


class MouseCollector:
    def __init__(self, callback, move_interval: float = 0.02):
        self.callback = callback
        self.move_interval = move_interval
        self._last_move_time = 0.0
        self._listener = Listener(
            on_click=self.on_click,
            on_move=self.on_move,
        )

    def start(self):
        self._listener.start()

    def stop(self):
        self._listener.stop()

    def on_click(self, x, y, button, pressed):
        data = {
            "type": "click",
            "button": str(button),
            "pressed": pressed,
            "x": x,
            "y": y,
            "timestamp": time.time(),
        }
        self.callback(data)

    def on_move(self, x, y):
            return


