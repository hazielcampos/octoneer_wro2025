
from components.Motor import forward, backward, stop_motors, start as start_pwm
import time
import keyboard
from components.Servo import set_angle, CENTER_POSITION, RIGHT_POSITION, LEFT_POSITION


speed = 30
def increase_speed(amount):
    global speed
    speed = min(speed + amount, 100)

def decrease_speed(amount):
    global speed
    speed = max(speed - amount, 10)

def main():
    start_pwm()
    while True:
        if keyboard.is_pressed("w"):
            forward(speed)
        elif keyboard.is_pressed("s"):
            backward(speed)
        if keyboard.is_pressed("d"):
            set_angle(RIGHT_POSITION)
        elif keyboard.is_pressed("a"):
            set_angle(LEFT_POSITION)
        else:
            set_angle(CENTER_POSITION)
            
        if keyboard.is_pressed("space"):
            stop_motors()
        if keyboard.is_pressed("e"):
            increase_speed(10)
        elif keyboard.is_pressed("q"):
            decrease_speed(10)
    
try:
    main()
except KeyboardInterrupt:
    stop_motors()
    print("User interrupt")

