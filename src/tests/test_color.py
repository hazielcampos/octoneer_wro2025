from Components.ColorSensor import ColorSensor
import time
import os
color = ColorSensor()
color.start()
def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def process_color_sensor():
    clear()
    r, g, b, c = color.color
    total = r + g + b
    if total == 0:
        return  # evitar división por cero
    
    # Normalizar valores RGB
    r_norm = r / total
    g_norm = g / total
    b_norm = b / total

    # Umbrales con tolerancia ±0.05
    # Naranja aproximado: r=0.394, g=0.34, b=0.28
    is_orange = (0.35 <= r_norm <= 0.44) and \
                (0.29 <= g_norm <= 0.39) and \
                (0.23 <= b_norm <= 0.33)

    # Azul aproximado: r=0.28, g=0.33, b=0.39
    is_blue = (0.23 <= r_norm <= 0.33) and \
              (0.28 <= g_norm <= 0.38) and \
              (0.34 <= b_norm <= 0.44)

    # Llamar a funciones de giro solo si el color actual no coincide con el giro en curso
    if is_orange:
        clear()
        print("Orange detected")
    elif is_blue:
        clear()
        print("Blue detected")
        
    time.sleep(0.1)
try:
    print("Press Ctrl-C to stop")
    while True:
        process_color_sensor()
except KeyboardInterrupt:
    pass