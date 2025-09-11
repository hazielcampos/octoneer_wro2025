
import threading
import time
import SensorsManager
from Components.Motor import forward, stop_motors, start as start_pwm
from Components.Servo import set_angle, CENTER_POSITION, LEFT_POSITION, RIGHT_POSITION, disable as disable_servo

is_turning = False

# =========================
# State variables
# =========================
is_running = False
finished = False
def set_active(active: bool):
    global is_running
    is_running = active        
turn_color = None

color_vuelta = "ninguno"

def on_orange_detected():
    global is_turning, turn_color
    if not is_running:
        return

    if is_turning:
        if turn_color != "orange":
            # el giro comenzó en azul y naranja indica fin del giro
            print("Fin del giro izquierdo, reseteando")
            is_turning = False
            turn_color = "ninguno"
            time.sleep(1)
            set_angle(CENTER_POSITION)
    else:
        # inicia giro a la derecha
        print("Iniciando giro a la derecha")
        is_turning = True
        turn_color = "orange"
        set_angle(RIGHT_POSITION)
        forward(1)
        time.sleep(0.5)
                
def on_blue_detected():
    global is_turning, turn_color
    if not is_running:
        return

    if is_turning:
        if turn_color != "blue":
            # el giro comenzó en naranja y azul indica fin del giro
            print("Fin del giro derecho, reseteando")
            is_turning = False
            turn_color = "ninguno"
            time.sleep(1)
            set_angle(CENTER_POSITION)
    else:
        # inicia giro a la izquierda
        print("Iniciando giro a la izquierda")
        is_turning = True
        turn_color = "blue"
        set_angle(LEFT_POSITION)
        forward(1)
        time.sleep(0.5)
        

# =========================
# PID variables
# =========================
Kp = 0.04   # Proporcional
Ki = 0.0   # Integral
Kd = 0.01   # Derivativo

integral = 0
last_error = 0
last_time = time.time()

def PID_control():
    global integral, last_error, last_time

    # Calcular error (positivo si está más lejos de lo deseado)
    error = SensorsManager.get_error()
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

    set_angle(correction)
    # Debug
    #print(f"[PID] Error: {error} "
    #    f"Servo={correction}")
    
# =========================
# Threaded processing
# =========================
def thread_function():
    while not finished:
        
        if is_running:
            if color_vuelta == "naranja":
                on_orange_detected()
            elif color_vuelta == "azul":
                on_blue_detected()
            elif not is_turning:
                forward(1)
                PID_control()
            else:
                forward(1)
                
        else:
            stop_motors()
            set_angle(CENTER_POSITION)
            is_turning = False
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