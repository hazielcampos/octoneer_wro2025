# =========================
# Librerias
# =========================
import threading
import cv2
import numpy as np
from Components.ColorSensor import ColorSensor
from Components.Ultrasonic import Ultrasonic
import MechanicsManager 
import os
import time

def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')
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
def in_range(point, lower, upper):
    t, l = point
    return lower[0] <= t <= upper[0] and lower[1] <= l <= upper[1]

def process_color_sensor():
    # Obtener valores del sensor
    r, g, b, c = color.color  # raw values
    total = r + g + b
    if total == 0:
        return  # evitar división por cero
    
    # Normalizar valores RGB
    r_norm = r / total
    g_norm = g / total
    b_norm = b / total

    # Umbrales para naranja
    # Ajusta según tu sensor y condiciones de luz
    is_orange = r_norm > 0.45 and g_norm > 0.25 and b_norm < 0.2

    # Umbrales para azul
    is_blue = b_norm > 0.4 and r_norm < 0.25 and g_norm < 0.25

    # Lógica de giro basada en color detectado
    if is_orange and MechanicsManager.turn_color != "orange":
        MechanicsManager.on_orange_detected()
    elif is_blue and MechanicsManager.turn_color != "blue":
        MechanicsManager.on_blue_detected()
    
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
        process_color_sensor()
        
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