# =========================
# Librerias
# =========================
import threading
import cv2
from libs import betterTime as time2
import time
# ==========================
# Constantes
# ==========================
LINE_CENTER = 0
LINE_LEFT = 1
LINE_RIGHT = 2
LINE_NONE = 3

# =========================
# Variables globales
# =========================
video = None
line_zone = "None"

# =========================
# Variables de estado
# =========================
is_running = False
finished = False
def set_active(active: bool):
    global is_running
    is_running = active
    
# ========================
# Funciones especificas del gestor de sensores
# =========================
def process_frame(frame):
    time.sleep(0.05)  # Simular procesamiento de frame

def get_line_zone():
    return line_zone

# =========================
# Funciones principales
# =========================

def thread_function():
    while not finished:
        if is_running:
            ret, frame = video.read()
            if not ret:
                break
            process_frame(frame)
            time.sleep(0.05)  # Esperar un poco antes de procesar el siguiente frame
        else:
            time2.sleep(0.1)  # Esperar si no está en ejecución
            

# =========================
# Hilo de procesamiento de video
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
    time.sleep(0.05)  # Esperar un poco para asegurarse de que el hilo se detenga
    video.release()
    cv2.destroyAllWindows()