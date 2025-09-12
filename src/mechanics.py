# ======================
# Important base imports
# ======================
import time

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
def run():
    forward(5)
    time.sleep(5)
    forward(10)
    time.sleep(4)
# ======================
# Base functions to handle multithreading
# ======================
def start():
    # Do something here before the main functions execution
    start_pwm()
    set_angle(CENTER_POSITION)
    
def cleanup():
    pass