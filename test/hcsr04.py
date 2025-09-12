from src.components.HCSR04 import HCSR04
from utils.terminal import clear
import time

right = HCSR04(24, 23)
left = HCSR04(5, 6)

try:
    while True:
        clear()
        print(f"D. Right: {right.distance}")
        print(f"D. Left: {left.distance}")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("User interrupt")