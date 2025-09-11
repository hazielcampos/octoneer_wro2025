
from Components.Motor import forward, stop_motors, start as start_pwm

def main():
    start_pwm()
    forward(50)
    input("Press Enter to stop motors...")
    forward(0)
    stop_motors()
    
try:
    main()
except KeyboardInterrupt:
    stop_motors()
