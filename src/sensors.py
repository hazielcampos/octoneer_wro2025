# ======================
# Important base imports
# ======================
import time
import threading
import shared

# ======================
# Imports
# ======================
import cv2
import numpy as np
from components.HCSR04 import HCSR04

# ======================
# CONSTANTS
# ======================
ECHO_R, TRIG_R = 24, 23
ECHO_L, TRIG_L = 5, 6

# ======================
# Sensors
# ======================
distance_right = HCSR04(ECHO_R, TRIG_R)
distance_left = HCSR04(ECHO_L, TRIG_L)

def generate_error():
    error = distance_left.distance - distance_right.distance
    
    return error


# ======================
# Main function
# ======================
def main():
    if shared.mode == shared.FREE_TEST:
        shared.set_error(generate_error())
    
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
    
    # Module thread start
    if not process_thread.is_alive():
        process_thread.start()
    
def cleanup():
    pass