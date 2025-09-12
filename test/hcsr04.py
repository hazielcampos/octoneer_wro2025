from src.components.HCSR04 import HCSR04
from src.utils.terminal import clear
import time

CENTER_POSITION = 52  # Neutral position of the servo
LEFT_POSITION = 62 # Left position of the servo
RIGHT_POSITION = 42  # Right position of the servo

Kp = 0.1
Ki = 0.0
Kd = 0.03

integral = 0
last_error = 0
last_time = time.time()

def PID_control(error):
    global integral, last_error, last_time

    # Tiempo transcurrido desde la última llamada
    now = time.time()
    dt = now - last_time if now - last_time > 0 else 1e-6

    # Componentes del PID
    proportional = Kp * error
    integral += Ki * error * dt
    derivative = Kd * (error - last_error) / dt

    output = proportional + integral + derivative

    # Actualizar memoria
    last_error = error
    last_time = now
    print(error)

    # Convertimos salida a corrección de servo
    correction = CENTER_POSITION + output

    # Limitar a rango permitido del servo
    correction = max(RIGHT_POSITION, min(LEFT_POSITION, correction))
    correction = int(round(correction))

    return correction

right = HCSR04(24, 23)
left = HCSR04(5, 6)

try:
    while True:
        clear()
        print(f"D. Right: {right.distance}")
        print(f"D. Left: {left.distance}")
        correction = PID_control(right.distance - left.distance)
        print(f"Correction: {correction}")
        time.sleep(0.04)
except KeyboardInterrupt:
    print("User interrupt")