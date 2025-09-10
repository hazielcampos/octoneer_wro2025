
from libs import GPIO
from libs import betterTime as time2
import threading
import time
import SensorsManager
from Components.Motor import forward, stop_motors, start as start_pwm
from Components.Servo import set_angle, CENTER_POSITION, LEFT_POSITION, RIGHT_POSITION, disable as disable_servo

is_turning = False
distance_threshold = 0  # Distance threshold in mm

def measure_center_distance():
    global distance_threshold
    distance_sum = 0
    samples = 5
    for i in range(samples):
        distance = SensorsManager.get_distance()
        distance_sum += distance
        time.sleep(0.1)
    final = distance_sum / samples
    distance_threshold = final
    return final
# =========================
# State variables
# =========================
is_running = False
finished = False
def set_active(active: bool):
    global is_running
    is_running = active        
    
# =========================
# PID variables
# =========================
Kp = 0.3   # Proporcional
Ki = 0.0   # Integral
Kd = 0.1   # Derivativo

integral = 0
last_error = 0
last_time = time.time()

def PID_control(target_distance, current_distance):
    global integral, last_error, last_time

    # Calcular error (positivo si está más lejos de lo deseado)
    error = target_distance - current_distance

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

    set_angle(correction)
    # Debug
    print(f"[PID] Target={target_distance:.1f}mm Current={current_distance:.1f}mm "
        f"Error={error:.1f} Out={output:.2f} Servo={correction}")
    
# =========================
# Threaded processing
# =========================
def thread_function():
    while not finished:
        if is_running:
            time.sleep(0.01)  # Ciclo rápido, no bloqueante
        else:
            stop_motors()
            set_angle(CENTER_POSITION)
            time.sleep(0.1)

process_thread = threading.Thread(target=thread_function, daemon=True)

def start():
    set_angle(CENTER_POSITION)
    start_pwm()
    
    if not process_thread.is_alive():
        process_thread.start()

def cleanup():
    global finished
    disable_servo()
    finished = True
    stop_motors()