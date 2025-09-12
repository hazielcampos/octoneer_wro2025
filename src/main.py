import threading
import cv2
import time
from components.Motor import forward, stop_motors, start as start_pwm
from components.Buttton import Button
from detection_functions import trigger_line
from components.Servo import set_angle, CENTER_POSITION, RIGHT_POSITION, LEFT_POSITION
is_running = False
stop_threads = False

btn = Button(17, True)

def btn_callback():
    global is_running
    is_running = not is_running
btn.set_callback(btn_callback)

def callback_1():
    set_angle(LEFT_POSITION)
def callback_2():
    set_angle(CENTER_POSITION)

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
        trigger_line(hsv, frame, callback_1, callback_2)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_threads = True
            break

    cap.release()
    cv2.destroyAllWindows()

def mechanics():
    start_pwm()
    while not stop_threads:
        if is_running:
            forward(20)
            time.sleep(1)
        else:
            stop_motors()

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
