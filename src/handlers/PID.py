import time
from components.Servo import CENTER_POSITION, RIGHT_POSITION, LEFT_POSITION
from enums.enums import Lane
Kp = 0.5
Ki = 0.0
Kd = 0.1


integral = 0
last_error = 0
last_time = time.time()

def map_error_to_servo_correction(error, max_error=100, max_servo_correction=13):
    """
    Mapea el error de ultrasonicos (-100 a +100) a corrección de servo limitada
    max_servo_correction: máxima corrección en grados desde el centro (52°)
    """
    # Limitar el error al rango esperado
    error = max(-max_error, min(max_error, error))
    
    # Mapear proporcionalmente al rango de corrección del servo
    servo_correction = (error / max_error) * max_servo_correction
    
    return servo_correction

def quantize_to_discrete_steps(correction, center=CENTER_POSITION, step_size=2, min_val=RIGHT_POSITION, max_val=LEFT_POSITION):
    """
    Convierte la corrección continua a pasos discretos de step_size grados
    centrados en center, con límites min_val y max_val
    """
    # Calcular el error respecto al centro
    error_from_center = correction - center
    
    # Si el error es menor a 1 grado, no hacer corrección
    if abs(error_from_center) < 1:
        return center
    
    # Redondear al múltiplo más cercano de step_size
    steps = round(error_from_center / step_size)
    
    # Si el redondeo resulta en 0 pero había error, forzar al menos un step
    if steps == 0 and abs(error_from_center) >= 1:
        steps = 1 if error_from_center > 0 else -1
    
    # Calcular la nueva posición
    new_position = center + (steps * step_size)
    
    # Aplicar límites
    new_position = max(min_val, min(max_val, new_position))
    
    return int(new_position)

def PID_control(error, lane):
    global integral, last_error, last_time
    if lane == Lane.RIGHT:
        error = error - 40
    elif lane == Lane.LEFT:
        error = error +40
    # Tiempo transcurrido desde la última llamada
    now = time.time()
    dt = now - last_time if now - last_time > 0 else 1e-6

    # Mapear el error de ultrasonicos a corrección de servo
    mapped_error = map_error_to_servo_correction(error)

    # Componentes del PID (ahora con error mapeado)
    proportional = Kp * mapped_error
    integral += Ki * mapped_error * dt
    derivative = Kd * (mapped_error - last_error) / dt

    output = proportional + integral + derivative

    # Actualizar memoria (usar el error mapeado para consistencia)
    last_error = mapped_error
    last_time = now

    # Convertimos salida a posición de servo
    correction = CENTER_POSITION + output

    # Limitar a rango permitido del servo
    correction = max(RIGHT_POSITION, min(LEFT_POSITION, correction))
    
    # Aplicar cuantización discreta
    discrete_correction = quantize_to_discrete_steps(correction)

    return discrete_correction
