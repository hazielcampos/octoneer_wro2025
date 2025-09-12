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
running_flag = False
# ======================
# Main function
# ======================
def main():
    global running_flag
    running_flag = True
    forward(10)
    time.sleep(3)
    forward(20)
    time.sleep(3)
    print("Running at base speed")
    forward(BASE_SPEED)
    time.sleep(2)  # Dale más tiempo para alcanzar y mantener la velocidad
    
    print("Stopping the motors")
    stop_motors()
    time.sleep(0.5)  # Pequeña pausa antes de reiniciar
    running_flag = False

# ======================
# Base module functions to make it work
# probably you don't have to touch this code too much
# ======================
def thread_function():
    while True:
        if shared.is_running and not running_flag:
            main()
        elif not shared.is_running:
            # Do something else
            stop_motors()
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