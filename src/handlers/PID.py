import time
from components.Servo import CENTER_POSITION, RIGHT_POSITION, LEFT_POSITION

Kp = 0.04
Ki = 0.0
Kd = 0.01

integral = 0
last_error = 0
last_time = time.time()

def PID_control(error):
    global integral, last_error, last_time

    # Calcular error (positivo si está más lejos de lo deseado)
    if error > 150 or error < -150:
        error = 0.0

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

    # Convertimos salida a corrección de servo
    correction = CENTER_POSITION + output

    # Limitar a rango permitido del servo
    correction = max(RIGHT_POSITION, min(LEFT_POSITION, correction))
    correction = int(round(correction))

    return correction