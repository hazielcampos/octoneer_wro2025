# =========================
# Librerias
# =========================
import threading
import cv2
from libs import betterTime as time2
import numpy as np
from utils.i2c_manager import i2c
from Components.DistanceSensor import DistanceSensor
import Components.ColorSensor as ColorSensor
# ==========================
# Contants
# ==========================
OBSTACLE_NONE = 0
OBSTACLE_GREEN = 1
OBSTACLE_RED = 2

# =======================
# Distance sensor
# =======================
sensor_right = DistanceSensor(xshut_pin=22, new_address=0x30)
sensor_left = DistanceSensor(xshut_pin=27, new_address=0x31)

def get_left_distance() -> float:
    return sensor_left.get_distance()

def get_right_distance() -> float:
    return sensor_right.get_distance()


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
lowerOrange_r, lowerOrange_g, lowerOrange_b, lowerOrange_c, lowerOrange_temp, lowerOrange_lux = 0, 100, 100
upperOrange_r, upperOrange_g, upperOrange_b, upperOrange_c, upperOrange_temp, upperOrange_lux = 20, 255, 255

lowerBlue_r, lowerBlue_g, lowerBlue_b, lowerBlue_c, lowerBlue_temp, lowerBlue_lux = 100, 150, 0
upperBlue_r, upperBlue_g, upperBlue_b, upperBlue_c, upperBlue_temp, upperBlue_lux = 140, 255, 255
def process_color_sensor():
    (r, g, b, c), temp, lux = ColorSensor.sensor_read()
    
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