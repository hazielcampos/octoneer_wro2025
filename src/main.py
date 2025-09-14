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
"""hey yo wt"""

import threading
import cv2
import time
from components.Motor import backward, forward, stop_motors, start as start_pwm
from components.HCSR04 import HCSR04
from components.Buttton import Button
from detection_functions import trigger_line, reset_last_callback, invert_last_callback
from components.Servo import set_angle, CENTER_POSITION, RIGHT_POSITION, LEFT_POSITION
from handlers.PID import PID_control

is_running = False
stop_threads = False
is_turning = False
turns = 0

ORIEN_H = 0
ORIEN_AH = 1
ORIEN_NONE = 2

orientation = ORIEN_NONE

btn = Button(17, True)

def btn_callback():
    global is_running
    is_running = not is_running
btn.set_callback(btn_callback)

def callback_1():
    if not is_running:
        return
    global orientation, turns
    if orientation ==ORIEN_NONE:
        orientation = ORIEN_AH
    elif orientation ==ORIEN_H:
        turns += 1

def callback_2():
    if not is_running:
        return
    global orientation, turns
    if orientation == ORIEN_NONE:
        orientation = ORIEN_H
    elif orientation == ORIEN_AH:
        turns += 1

def vision():
    global stop_threads
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    while not stop_threads:
        ret, frame = cap.read()
        if not ret:
            continue
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.equalizeHist(v)
        hsv = cv2.merge([h, s, v])
        
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
        trigger_line(is_running, hsv, frame, callback_1, callback_2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_threads = True
            break

    cap.release()
    cv2.destroyAllWindows()

sensor_right = HCSR04(24, 23)
sensor_left = HCSR04(5, 6)

TURN_THRESHOL = 100
NEXT_CURVE_THRESHOL = 2
turn_end_delay = 0.7
turn_end_start = 0
last_curve_time = 0

def mechanics():
    global orientation, turn_end_start, turns, is_running, is_turning, last_curve_time
    start_pwm()
    while not stop_threads:
        if is_running:
            left_dist = sensor_left.distance
            right_dist = sensor_right.distance
            if is_turning:
                forward(45)
                
                if turn_end_start > 0 and (time.time() - turn_end_start) > turn_end_delay:
                    set_angle(CENTER_POSITION)
                    turn_end_start = 0
                    last_curve_time = time.time()
                    is_turning = False
                    print("turn finished")
                    time.sleep(0.2)
            
            else:
                if left_dist > TURN_THRESHOL and (last_curve_time - time.time()) > NEXT_CURVE_THRESHOL:
                    set_angle(LEFT_POSITION)
                    print("[LOG] turn started LEFT")
                    is_turning = True
                    turn_end_start = time.time()
                
                elif right_dist > TURN_THRESHOL and (last_curve_time - time.time()) > NEXT_CURVE_THRESHOL:
                    set_angle(RIGHT_POSITION)
                    print("[LOG] turn started RIGHT")
                    is_turning = True
                    turn_end_start = time.time()
                else:
                    forward(40)
                    correction = PID_control(left_dist - right_dist)
                    set_angle(correction)

            laps = turns / 4
            if laps >= 3:
                # Final PID to center the robot and end
                print(f"finished at: {laps}")
                for i in range(5):
                    PID_control(sensor_left.distance - sensor_right.distance)
                    time.sleep(0.1)
                stop_motors()
                is_running = False
            time.sleep(0.05)
        else:
            stop_motors()
            set_angle(CENTER_POSITION)
            orientation = ORIEN_NONE
            turns = 0
            reset_last_callback()

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
    print("User interrupt")
finally:
    stop_threads = True
    stop_motors()
