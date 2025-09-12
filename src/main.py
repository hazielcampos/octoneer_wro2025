import Rasp.GPIO as GPIO
import mechanics as mechanics
import sensors as sensors
import time
from components.Buttton import Button

# =========================
# Button sensor configuration
# =========================

button = Button(17, True)

def btn_callback():
    print("Btn state changed")

button.set_callback(btn_callback)

def main():
    while True:
        time.sleep(0.1)

    
try:
    main()
except KeyboardInterrupt:
    print("Interrupción del usuario, limpiando...")
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    print("Sistema detenido correctamente.")