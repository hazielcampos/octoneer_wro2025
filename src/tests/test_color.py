from Components.ColorSensor import sensor_read
import time

try:
    print("Press Ctrl-C to stop")
    while True:
        (r, g, b, c), temp, lux = sensor_read()
        print(f"R: {r}, G: {g}, B: {b}, C: {c}, Temp: {temp}, Lux: {lux}")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass