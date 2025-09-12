# ======================
# Important base imports
# ======================
import shared
import time
import threading

# ======================
# Imports
# ======================
from components.Motor import forward, stop_motors, start as start_pwm
from components.Servo import set_angle, CENTER_POSITION, LEFT_POSITION, RIGHT_POSITION, disable as disable_servo

# ======================
# CONSTANTS
# ======================
BASE_SPEED = 40

# ======================
# Main function
# ======================
def main():
    print("Running at really low speed")
    forward(10)
    time.sleep(1)
    print("Speed increased to 20")
    forward(20)
    time.sleep(1)
    print("Running pwm at base speed")
    forward(BASE_SPEED)
    time.sleep(1)
    print("Increasing speed by 10")
    forward(BASE_SPEED + 10)
    time.sleep(1)
    print("Stopping the motors")
    stop_motors()
    print("Wait 3 seconds to restart")
    time.sleep(3)

# ======================
# Base module functions to make it work
# probably you don't have to touch this code too much
# ======================
def thread_function():
    while True:
        if shared.is_running:
            main()
            time.sleep(0.01)
        else:
            # Do something else
            time.sleep(0.01)
# ======================
# Base functions to handle multithreading
# ======================
process_thread = threading.Thread(target=thread_function, daemon=True)
def start():
    # Do something here before the main functions execution
    start_pwm()
    set_angle(CENTER_POSITION)
    
    # Module thread start
    if not process_thread.is_alive():
        process_thread.start()
    
def cleanup():
    pass