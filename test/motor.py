
from src.components.Motor import forward, stop_motors, start as start_pwm
import time


def main():
    start_pwm()
    while True:
        speed = int(input("Enter a speed"))
        
        forward(speed)
        time.sleep(0.3)
    
try:
    main()
except KeyboardInterrupt:
    stop_motors()
    print("User interrupt")

