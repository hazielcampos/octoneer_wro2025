# =========================
# Librerias
# =========================
import threading
import cv2
from libs import betterTime as time2
import time
import numpy as np
import MechanicsManager
# ==========================
# Contants
# ==========================
LINE_CENTER = 0
LINE_LEFT = 1
LINE_RIGHT = 2
LINE_NONE = 3

CURVE_NONE = 0
CURVE_ORANGE = 1
CURVE_BLUE = 2

TURNING = 0
GOING_STRAIGHT = 1
PARKING = 2

STATUS = GOING_STRAIGHT
CURVE_TYPE = CURVE_NONE


OBSTACLE_NONE = 0
OBSTACLE_GREEN = 1
OBSTACLE_RED = 2

WALL_TO_LEFT = 1
WALL_TO_RIGHT = 2
WALL_NONE = 0



# =========================
# Global variables
# =========================
video = None
line_zone = "None"
line_position = 0
curve_indication = CURVE_NONE
obstacle_detected = OBSTACLE_NONE
wall_correction = 0

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
lWall_h, lWall_s, lWall_v = 0, 0, 0
uWall_h, uWall_s, uWall_v = 124, 255, 41
def walls(frame) -> list[tuple[float, float]]: # returns the x, y of the walls detected
    return []

lOrange_h, lOrange_s, lOrange_v = 6, 51, 134
uOrange_h, uOrange_s, uOrange_v = 13, 139, 188

orange_lower = (lOrange_h, lOrange_s, lOrange_v)
orange_upper = (uOrange_h, uOrange_s, uOrange_v)

lBlue_h, lBlue_s, lBlue_v = 112, 0, 21
uBlue_h, uBlue_s, uBlue_v = 136, 169, 80
blue_lower = (lBlue_h, lBlue_s, lBlue_v)
blue_upper = (uBlue_h, uBlue_s, uBlue_v)
last_curves = None

def detect_orange(hsv, frame) -> list[tuple[int, float, np.ndarray]]:
    """Detecta curvas naranjas, dibuja contornos y devuelve (tipo, área, contorno)"""
    curves = []
    mask = cv2.inRange(hsv, orange_lower, orange_upper)
    # Mostrar máscara opcional
    #cv2.imshow("Orange Mask", mask)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1:
            #cv2.drawContours(frame, [cnt], -1, (0, 165, 255), 2)  # naranja
            curves.append((CURVE_ORANGE, area, cnt))
    return curves

def detect_blue(hsv, frame) -> list[tuple[int, float, np.ndarray]]:
    """Detecta curvas azules, dibuja contornos y devuelve (tipo, área, contorno)"""
    curves = []
    mask = cv2.inRange(hsv, blue_lower, blue_upper)
    # Mostrar máscara opcional
    #cv2.imshow("Blue Mask", mask)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1:
            #cv2.drawContours(frame, [cnt], -1, (255, 0, 0), 2)  # azul
            curves.append((CURVE_BLUE, area, cnt))
    return curves

def curve_indicators(hsv, frame) -> list[tuple[int, float, np.ndarray]]:
    """
    Combina ambas detecciones (naranja y azul) pero procesadas por separado.
    """
    if MechanicsManager.is_turning:
        return last_curves if last_curves is not None else []
    
    curves = []
    curves += detect_orange(hsv, frame)
    curves += detect_blue(hsv, frame)
    
    return curves

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

ignored_x1, ignored_x2 = 0, 1280
ignored_y1, ignored_y2 = 525, 720

def draw_layout(frame):
    cv2.rectangle(frame, (ignored_x1, ignored_y1), (ignored_x2, ignored_y2), (0, 255, 255), 2)
    
def process_frame(hsv,frame):
    global STATUS, CURVE_TYPE, last_curves
    curves = curve_indicators(hsv, frame)
    if MechanicsManager.is_turning:
        curves = last_curves if last_curves is not None else curves
    else:
        last_curves = curves
    last_area = 0
    curve = CURVE_NONE
    min_area = 10
    for curve_type, area, cnt in curves:
        if area < min_area:
            curve= CURVE_NONE
            continue
        elif area > last_area:
            last_area = area
            curve = curve_type
    if curve != CURVE_NONE:
        cv2.putText(frame, f"Curve: {'ORANGE' if curve == CURVE_ORANGE else 'BLUE'}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        CURVE_TYPE = curve
        STATUS = TURNING
    
    #obstacle_type, obstacle_position = nearest_obstacle(frame)

def get_line_zone():
    return line_zone

# =========================
# Thread function
# =========================

def thread_function():
    global video
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    video.set(cv2.CAP_PROP_FPS, 30)
    
    ret, frame = video.read()

    if ret:  
        # Guarda la imagen en el directorio deseado
        cv2.imwrite("./frame_guardado.jpg", frame)
        print("✅ Frame guardado con éxito")
    else:
        print("❌ No se pudo capturar el frame")
    
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