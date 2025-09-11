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
    # Obtener valores del sensor
    r, g, b, c = color.color  # raw values
    total = r + g + b
    if total == 0:
        return  # evitar división por cero
    
    # Normalizar valores RGB
    r_norm = r / total
    g_norm = g / total
    b_norm = b / total
    clear()
    print(f"R norm: {r_norm}, G norm: {g_norm}, B norm: {b_norm}")
try:
    print("Press Ctrl-C to stop")
    while True:
        process_color_sensor()
except KeyboardInterrupt:
    pass