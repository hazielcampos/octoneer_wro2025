from src.components.HCSR04 import HCSR04
from src.utils.terminal import clear
import time


from src.handlers.PID import PID_control

right = HCSR04(24, 23)
left = HCSR04(5, 6)

try:
    while True:
        clear()
        print(f"D. Right: {right.distance}")
        print(f"D. Left: {left.distance}")
        correction = PID_control(right.distance - left.distance)
        print(f"Correction: {correction}")
        time.sleep(0.04)
except KeyboardInterrupt:
    print("User interrupt")