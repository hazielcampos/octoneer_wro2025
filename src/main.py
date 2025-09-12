
from src.components.Motor import forward, stop_motors, start as start_pwm
import time
from components.Buttton import Button

is_running = False

btn = Button(17, True)

def btn_callback():
    global is_running
    is_running = not is_running
btn.set_callback(btn_callback)

def main():
    start_pwm()
    while True:
        if is_running:
            forward(5)
            time.sleep(5)
            forward(10)
            time.sleep(5)
            forward(20)
            time.sleep(5)
            forward(40)
            time.sleep(5)
        else:
            stop_motors()     
    
try:
    main()
except KeyboardInterrupt:
    stop_motors()
    print("User interrupt")

