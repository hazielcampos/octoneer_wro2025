import Rasp.GPIO as GPIO
import mechanics as mechanics
import sensors as sensors
import time
import shared

# =========================
# Button sensor configuration
# =========================
input_io = 17  # GPIO pin to read the sensor state
GPIO.setup(input_io, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Setup button with pull-up

def get_button():
    return not GPIO.input(input_io)

def setup():
    sensors.start()
    mechanics.start()

def main():
    print("Robot iniciado con exito... el loop principal comenzara a ejecutarse.")
    loop()

def loop():
    global is_running
    while True:
        if get_button():
            shared.set_is_running(not shared.is_running)
            print(f"Sistema {'activado' if shared.is_running else 'desactivado'}")
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