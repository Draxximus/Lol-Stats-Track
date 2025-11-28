from pynput.mouse import Listener
import time


class MouseCollector:
    """
    Escucha el mouse en un hilo aparte.
    - start() -> inicia el listener (no bloquea)
    - stop()  -> detiene el listener
    """

    def __init__(self, callback, move_interval: float = 0.02):
        self.callback = callback
        self.move_interval = move_interval
        self._last_move_time = 0.0
        self._listener = Listener(
            on_click=self.on_click,
            on_move=self.on_move,
        )

    def start(self):
        """Inicia el listener en un hilo separado."""
        self._listener.start()

    def stop(self):
        """Detiene el listener."""
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

