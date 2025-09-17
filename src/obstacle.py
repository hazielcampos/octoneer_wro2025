"""
Codigo desarrollado por Haziel Vds
Malas palabras durante el desarrollo: 745
Tazas de cafe: 6
Horas de sueño: 2

El codigo hace lo siguiente:
- El robot se inicializa
- Espera a que opriman el boton
- Cuando se oprime el boton, comienza con PID hasta detectar el inicio de una curva
- Cuando detecta el inicio de una curva pone en servo en posicion para girar
- Sigue girando hasta que detecta el final de esa curva
- Al detectar el final de la curva, sin bloquear el hilo de video, espera unos segundos mas girando antes de enderezar
- Vuelve a comenzar con pid
- Esto se repite por 12 curvas o 3 vueltas
- El robot se detiene a la 3er vuelta
"""
# ==============================
# IMPORTS
# ==============================
import threading
import cv2
import time
from components.Motor import forward, stop_motors, start as start_pwm
from components.HCSR04 import HCSR04
from components.Buttton import Button
from detection_functions import trigger_line, reset_last_callback
from components.Servo import set_angle, CENTER_POSITION, RIGHT_POSITION, LEFT_POSITION
from handlers.PID import PID_control
from enums.enums import Orientation, Lane, Color
from Logger import get_logger
from clasifier import ObstacleClasifier
# ==============================
# CONSTANTS
# ==============================
TURN_THRESHOLD = 100
NEXT_CURVE_THRESHOLD = 1.2
TURN_END_DELAY = 1.2
AVERAGE_SPEED = 80
TURN_SPEED = 100
POST_END_CORRECTION_TIME = 1.5 # seconds


# ==============================
# STATE VARIABLES
# ==============================
is_running = False
stop_threads = False
is_turning = False
turns = 0
should_turn = False
orientation = Orientation.NO_SET
turn_end_start = 0
last_curve_time = 0
start_time = 0
current_lane = Lane.CENTER
next_obstacle = Color.NONE

# ==============================
# COMPONENTS
# ==============================
btn = Button(17, True)
sensor_right = HCSR04(24, 23)
sensor_left = HCSR04(5, 6)
Log = get_logger()

# ==============================
# CALLBACKS
# ==============================
def btn_callback():
    global is_running
    is_running = not is_running

def callback_1():
    if not is_running:
        return
    global orientation, turns, should_turn
    if orientation == Orientation.NO_SET:
        orientation = Orientation.COUNTERCLOCKWISE
    if orientation == Orientation.COUNTERCLOCKWISE:
        should_turn = True
    elif orientation == Orientation.CLOCKWISE:
        turns += 1

def callback_2():
    if not is_running:
        return
    global orientation, turns, should_turn
    if orientation == Orientation.NO_SET:
        orientation = Orientation.CLOCKWISE
    if orientation == Orientation.CLOCKWISE:
        should_turn = True
    elif orientation == Orientation.COUNTERCLOCKWISE:
        turns += 1

# ==============================
# COMPONENTS SETUP
# ==============================
btn.set_callback(btn_callback)
obstacleClasifier = ObstacleClasifier(((0, 150), (640, 300)))
obstacleClasifier.start()


# ==============================
# Computer Vision main function
# ==============================
def vision():
    global stop_threads, next_obstacle
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Camera can't be oppened")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    while not stop_threads:
        ret, frame = cap.read()
        if not ret:
            continue
        obstacleClasifier.set_frame(frame)
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.equalizeHist(v)
        hsv = cv2.merge([h, s, v])
        
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
        trigger_line(is_running, hsv, frame, callback_1, callback_2)
        
        
                
        obs = obstacleClasifier.get_nearest_box()
        if obs:
            area, (x, y, w, heigth), color, bgr = obs
            next_obstacle = color
        display = obstacleClasifier.get_display_frame()
        cv2.imshow("Frame", frame)
        cv2.imshow("Frame display", display)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_threads = True
            break

    cap.release()
    cv2.destroyAllWindows()

# ==============================
# Mechanics manager, control the motors and servo using the vision and sensors information
# ==============================
def mechanics():
    global orientation, turn_end_start, turns, is_running, is_turning, last_curve_time, should_turn, start_time, current_lane, next_obstacle
    start_pwm()
    while not stop_threads:
        if is_running:
            if start_time <= 0:
                start_time = time.time()
            left_dist = sensor_left.distance
            right_dist = sensor_right.distance
            if is_turning:
                forward(TURN_SPEED)
                delay = TURN_END_DELAY
                if current_lane == Lane.CENTER:
                    delay = TURN_END_DELAY / 1.5
                elif current_lane == Lane.CENTER:
                    delay = TURN_END_DELAY * 1.5
                    
                if turn_end_start > 0 and (time.time() - turn_end_start) > delay:
                    set_angle(CENTER_POSITION)
                    turn_end_start = 0
                    last_curve_time = time.time()
                    is_turning = False
                    Log.Info("Turn finished.")
                    should_turn = False
                    time.sleep(0.2)
                elif orientation == Orientation.CLOCKWISE and right_dist <= 10:
                    set_angle(LEFT_POSITION)
                    time.sleep(0.2)
                    set_angle(CENTER_POSITION)
                    turn_end_start = 0
                    last_curve_time = time.time()
                    is_turning = False
                    Log.Info("Turn finished.")
                    should_turn = False
                    time.sleep(0.2)
                elif orientation == Orientation.COUNTERCLOCKWISE and left_dist <= 10:
                    set_angle(RIGHT_POSITION)
                    time.sleep(0.2)
                    set_angle(CENTER_POSITION)
                    turn_end_start = 0
                    last_curve_time = time.time()
                    is_turning = False
                    Log.Info("Turn finished.")
                    should_turn = False
                
            
            
            else:
                can_turn_left = left_dist > TURN_THRESHOLD and (time.time() - last_curve_time) > NEXT_CURVE_THRESHOLD
                can_turn_right = right_dist > TURN_THRESHOLD and (time.time() - last_curve_time) > NEXT_CURVE_THRESHOLD
                if can_turn_left and should_turn and orientation == Orientation.COUNTERCLOCKWISE:
                    set_angle(LEFT_POSITION)
                    Log.Info("Turn started LEFT.")
                    is_turning = True
                    turn_end_start = time.time()
                
                elif can_turn_right and should_turn and orientation == Orientation.CLOCKWISE:
                    set_angle(RIGHT_POSITION)
                    Log.Info("Turn started RIGHT.")
                    is_turning = True
                    turn_end_start = time.time()
                else:
                    if next_obstacle == Color.RED:
                        current_lane = Lane.RIGHT
                    elif next_obstacle == Color.GREEN:
                        current_lane = Lane.LEFT
                    else:
                        current_lane = Lane.CENTER
                    
                    forward(AVERAGE_SPEED)
                    correction = PID_control(left_dist - right_dist, current_lane)
                    set_angle(correction)

            laps = turns / 4
            if laps >= 3:
                # Final PID to center the robot and end
                for i in range(int(round(POST_END_CORRECTION_TIME * 10))):
                    correction = PID_control(sensor_left.distance - sensor_right.distance, current_lane)
                    set_angle(correction)
                    time.sleep(0.1)
                stop_motors()
                Log.Info(f"Finished with total laps of: {laps}")
                Log.Info(f"Total run time: {time.time() - start_time} seconds.")
                is_running = False
                time.sleep(0.2)
            time.sleep(0.01)
        else:
            stop_motors()
            set_angle(CENTER_POSITION)
            orientation = Orientation.NO_SET
            turns = 0
            reset_last_callback()
            should_turn = False
            start_time = 0
            next_obstacle = Color.NONE

# =============================================================
# MAIN FUNCTION
# =============================================================

def main():
    thread_mechanics = threading.Thread(target=mechanics, daemon=True)
    thread_vision = threading.Thread(target=vision)
    
    thread_mechanics.start()
    thread_vision.start()
    
    while not stop_threads:
        time.sleep(0.1)

try:
    main()
except KeyboardInterrupt:
    Log.Warn("User interrupt.")
finally:
    stop_threads = True
    stop_motors()
