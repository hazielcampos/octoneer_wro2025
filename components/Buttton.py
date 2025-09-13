import Rasp.GPIO as GPIO
import time
import threading
from typing import Callable

class Button:
    def __init__(self, GPIO_IN: int, pull_up=True):
        self.pin = GPIO_IN
        self.pressed = False
        self.callback: Callable[[], None] | None = None

        if pull_up:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        else:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.thread = threading.Thread(target=self.thread_function, daemon=True)
        self.thread.start()

    def set_callback(self, callback: Callable[[], None]):
        self.callback = callback

    def thread_function(self):
        last_state = GPIO.input(self.pin)
        try:
            while True:
                state = GPIO.input(self.pin)
                if state != last_state:  # detecta cambio
                    self.pressed = not state  # si pull_up: LOW = presionado
                    if self.pressed and self.callback:
                        self.callback()
                    last_state = state
                time.sleep(0.05)  # debounce
        except Exception as e:
            print(f"Something went wrong with the button: {e}")