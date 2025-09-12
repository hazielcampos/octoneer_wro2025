
from src.components.Motor import forward, stop_motors, start as start_pwm
import time
from components.Buttton import Button
import threading
import cv2

is_running = False

btn = Button(17, True)

def btn_callback():
    global is_running
    is_running = not is_running
btn.set_callback(btn_callback)

def vision():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    while True:
        ret, frame = cap.read()
        cv2.imshow("Frame", frame)
        time.sleep(0.1)

def mechanics():
    start_pwm()
    while True:
        if is_running:
            forward(5)
            time.sleep(5)
            forward(10)
            time.sleep(5)
            forward(20)
            time.sleep(5)
            forward(40)
            time.sleep(5)
        else:
            stop_motors()
thread_mechanics = threading.Thread(target=mechanics, daemon=True)
thread_vision = threading.Thread(target=vision, daemon=True)
            
def main():
    thread_mechanics.start()
    thread_vision.start()
    
    while True:
        time.sleep(0.1) 
    
try:
    main()
except KeyboardInterrupt:
    stop_motors()
    print("User interrupt")

