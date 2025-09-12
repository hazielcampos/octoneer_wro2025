
from components.Motor import forward, stop_motors, start as start_pwm
import time


def main():
    start_pwm()
    while True:
        pwm = int(input("Enter pwm value:"))
        
        forward(50) # Inertia breaker pulse
        time.sleep(0.7)
        forward(pwm)
        input("Press Enter to stop motors...")
        stop_motors()
        time.sleep(0.1)
    
try:
    main()
except KeyboardInterrupt:
    stop_motors()
    print("User interrupt")

