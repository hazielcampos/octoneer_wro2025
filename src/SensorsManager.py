# =========================
# Librerias
# =========================
import threading
import cv2
import numpy as np
from Components.ColorSensor import ColorSensor
from Components.Ultrasonic import Ultrasonic
# ==========================
# Contants
# ==========================
OBSTACLE_NONE = 0
OBSTACLE_GREEN = 1
OBSTACLE_RED = 2

# =======================
# Distance sensor
# =======================
sensor_right = Ultrasonic(23, 24)
sensor_left = Ultrasonic(6, 5)
sensor_right.start()
sensor_left.start()

def get_left_distance() -> float:
    return sensor_left.distance

def get_right_distance() -> float:
    return sensor_right.distance

color = ColorSensor()
color.start()

""" Returns the difference between the left and right distance sensors.
If the right distance is greater than the left distance, the result will be negative.
else it will be positive.

This value can be used to determine the direction to turn to center the robot between two walls.
For example, if the result is negative, the robot should turn left to center itself.
If the result is positive, the robot should turn right to center itself.
If the result is zero, the robot is centered between the two walls.
"""
# if the error is more than this value, the error is considered zero bc probably it is the start of a curve so we have to wait
# for the color sensor to detect the curve start line indicator
max_error_to_get_zero = 20 # cm
def get_error() -> float:
    error = get_left_distance() - get_right_distance() # convert mm to cm
    #if abs(error) > max_error_to_get_zero:
    #    return 0.0
    return error
# =========================
# Global variables
# =========================
video = None
# =========================
# State variables
# =========================
is_running = False
finished = False
def set_active(active: bool):
    global is_running
    is_running = active
    
# ========================
# Specific functions of the Sensor Manager
# =========================
lParking_h, lParking_s, lParking_v = 0, 0, 0
uParking_h, uParking_s, uParking_v = 0, 0, 0
def parking_slot(frame) -> tuple[float, float]: # returns de x, y of the parking slot center
    return (0.0, 0.0)

lGreen_h, lGreen_s, lGreen_v = 35, 22, 50
uGreen_h, lGreen_s, lGreen_v = 82, 139, 126

lRed_h, lRed_s, lRed_v = 0, 112, 87
uRed_h, uRed_s, uRed_v = 179, 187, 133
def nearest_obstacle(frame) -> tuple[int, tuple[int, int]]: # returns OBSTACLE_NONE, OBSTACLE_GREEN or OBSTACLE_RED
    return OBSTACLE_NONE, (0, 0)
    
def process_frame(hsv,frame):
    pass
lowerOrange_r, lowerOrange_g, lowerOrange_b, lowerOrange_c, lowerOrange_temp, lowerOrange_lux = 0, 100, 100, 0, 0, 0
upperOrange_r, upperOrange_g, upperOrange_b, upperOrange_c, upperOrange_temp, upperOrange_lux = 20, 255, 255, 0, 0, 0

lowerBlue_r, lowerBlue_g, lowerBlue_b, lowerBlue_c, lowerBlue_temp, lowerBlue_lux = 100, 150, 0, 0, 0, 0
upperBlue_r, upperBlue_g, upperBlue_b, upperBlue_c, upperBlue_temp, upperBlue_lux = 140, 255, 255, 0, 0, 0
def process_color_sensor():
    (r, g, b, c), temp, lux = color.get_color()
    
    # cuando detecta naranja llamar a MechanicsManager.on_orange_detected()
    # cuando detecta azul llamar a MechanicsManager.on_blue_detected()
    
# =========================
# Thread function
# =========================

def thread_function():
    global video
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    video.set(cv2.CAP_PROP_FPS, 30)
    
    ret, frame = video.read()

    while not finished:
        ret, frame = video.read()
        if not ret:
            break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        
        frame_display = frame.copy()
        
        process_frame(hsv, frame_display)
        
        #cv2.imshow("Frame", frame_display)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# =========================
# Video capture and thread management
# =========================
process_thread = threading.Thread(target=thread_function, daemon=True)
def start():
    global video
    if video is not None:
        video.release()
    if not process_thread.is_alive():
        process_thread.start()

def cleanup():
    global finished
    finished = True
    if video is not None:
        video.release()
    cv2.destroyAllWindows()
    if process_thread.is_alive():
        process_thread.join()