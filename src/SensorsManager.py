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
    time.sleep(0.05)  # Simulate processing delay

def get_line_zone():
    return line_zone

# =========================
# Thread function
# =========================

def thread_function():
    while not finished:
        if is_running:
            ret, frame = video.read()
            if not ret:
                break
            process_frame(frame)
            time.sleep(0.05)  # Wait a bit before processing the next frame
        else:
            time2.sleep(0.1)  # Wait if not active
            

# =========================
# Video capture and thread management
# =========================
process_thread = threading.Thread(target=thread_function, daemon=True)
def start():
    global video
    if video is not None:
        video.release()
    video = cv2.VideoCapture(0)
    if not process_thread.is_alive():
        process_thread.start()

def cleanup():
    global finished
    finished = True
    time.sleep(0.05)  # Wait for the thread to finish
    video.release()
    cv2.destroyAllWindows()