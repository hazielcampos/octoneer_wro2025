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

# =========================
# Global variables
# =========================
video = None
line_zone = "None"
line_position = 0

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
def process_frame(frame):
    global line_position
    roi = frame[140:230, 100:580]  # Adjust according to your camera
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    lower_blue = (20, 30, 40)
    upper_blue = (140, 255, 255)
    
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    M = cv2.moments(mask)
    if M["m00"] > 0:
        cx = int(M["m10"] / M["m00"])
        
        x = cx - (roi.shape[1] // 2)
        line_position = x / (roi.shape[1] // 2)
    
    cv2.putText(frame, f"Zona: {line_zone}", (10, 460), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return mask, frame
    

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
        mask, frame2 = process_frame(frame)
        cv2.imshow("Mask", mask)
        cv2.imshow("Camera Feed", frame2)
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