from libs import GPIO, betterTime as time2
import MechanicsManager as mechanics
import SensorsManager as sensors
import time

# =========================
# Button sensor configuration
# =========================
input_io = 17  # GPIO pin to read the sensor state
GPIO.setup(input_io, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Setup button with pull-up

def get_button():
    return not GPIO.input(input_io)

is_running = False

def setup():
    sensors.start()
    mechanics.start()

def main():
    loop()

def global_active(is_active: bool):
    sensors.set_active(is_active)
    mechanics.set_active(is_active)
    time2.set_active(is_active)

def loop():
    global is_running
    while True:
        if get_button():
            is_running = not is_running
            global_active(is_running)
            print(f"Sistema {'activado' if is_running else 'desactivado'}")
            time.sleep(0.5)  # Debounce delay

def cleanup():
    sensors.cleanup()
    mechanics.cleanup()
    GPIO.cleanup()
    
try:
    setup()
    main()
except KeyboardInterrupt:
    print("Interrupción del usuario, limpiando...")
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    cleanup()
    print("Sistema detenido correctamente.")