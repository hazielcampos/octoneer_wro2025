
from components.Motor import forward, stop_motors, start as start_pwm
import time


def main():
    start_pwm()
    while True:
        forward(5)
        input("Press Enter to next speed...")
        forward(10)
        input("Press Enter to next speed...")
        forward(20)
        input("Press Enter to next speed...")
        forward(40)
        input("Press Enter to next speed...")
        
    
try:
    main()
except KeyboardInterrupt:
    stop_motors()
    print("User interrupt")

