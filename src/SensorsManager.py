# =========================
# Librerias
# =========================
import threading
import cv2
from libs import betterTime as time2
import time
# ==========================
# Contants
# ==========================
LINE_CENTER = 0
LINE_LEFT = 1
LINE_RIGHT = 2
LINE_NONE = 3

CURVE_NONE = 0
CURVE_STARTS = 1
CURVE_ENDS = 2

# =========================
# Global variables
# =========================
video = None
line_zone = "None"
line_position = 0
curve_indication = CURVE_NONE

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
def get_curve_indication(frame):
    global curve_indication
    
    x1, y1 = 200, 140
    x2, y2 = 480, 230
    
    roi = frame[y1:y2, x1:x2]  # Adjust according to your camera
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2) # Draw rectangle for ROI
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_blue = (20, 30, 40)
    upper_blue = (140, 255, 255)
    lower_orange = (0, 50, 50)
    upper_orange = (20, 255, 255)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    
    blue_pixels = cv2.countNonZero(mask_blue)
    orange_pixels = cv2.countNonZero(mask_orange)
    
    cv2.putText(frame, f"Azul: {blue_pixels}", (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, f"Naranja: {orange_pixels}", (10, 90), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 140, 255), 2)
    
    blue_detected = blue_pixels > 500
    orange_detected = orange_pixels > 500
    
    if blue_detected:
        curve_indication = CURVE_STARTS
    elif orange_detected:
        curve_indication = CURVE_ENDS
    else:
        curve_indication = CURVE_NONE
    
    cv2.putText(frame, f"Curva: {curve_indication}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Mask blue", mask_blue)
    cv2.imshow("Mask orange", mask_orange)
        

def get_line_position(frame):
    global line_position
    roi = frame[140:230, 200:480]  # Adjust according to your camera
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    lower_blue = (20, 30, 40)
    upper_blue = (140, 255, 255)
    
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    M = cv2.moments(mask)
    if M["m00"] > 0:
        cx = int(M["m10"] / M["m00"])
        
        x = cx - (roi.shape[1] // 2)
        line_position = x / (roi.shape[1] // 2)
    
    cv2.putText(frame, f"Posicion: {line_position}", (10, 460), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Mask line", mask)  

def process_frame(frame):
    get_curve_indication(frame)
    get_line_position(frame)

def get_line_zone():
    return line_zone

# =========================
# Thread function
# =========================

def thread_function():
    global video
    video = cv2.VideoCapture(0)
    while not finished:
        ret, frame = video.read()
        if not ret:
            break
        process_frame(frame)
        cv2.imshow("Frame", frame)
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