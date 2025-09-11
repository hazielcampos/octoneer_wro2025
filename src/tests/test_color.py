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

try:
    print("Press Ctrl-C to stop")
    while True:
        (r, g, b, c), temp, lux = color.color, color.temp, color.lux
        clear()
        print(f"R: {r}, G: {g}, B: {b}, C: {c}, Temp: {temp}, Lux: {lux}")
        time.sleep(0.1)
except KeyboardInterrupt:
    pass