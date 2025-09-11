import time
from libs.GPIO import GPIO
import threading

class Ultrasonic:
    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo
        self.distance = 0.0
        self.thread = None
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.output(self.trig, False)
        time.sleep(0.0002)
    
    def start(self):
        self.thread = threading.Thread(target=self.thread_function, daemon=True)
        self.thread.start()
    
    def measure_distance(self, timeout=0.02) -> float:
        # Pulso de trigger
        GPIO.output(self.trig, False)
        time.sleep(0.000002)
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        start_time = time.time()

        # Esperar a que empiece el pulso
        while GPIO.input(self.echo) == 0:
            if time.time() - start_time > timeout:
                return None
        pulse_start = time.time()

        # Esperar a que termine el pulso
        while GPIO.input(self.echo) == 1:
            if time.time() - pulse_start > timeout:
                return None
        pulse_end = time.time()

        # Duración del pulso
        duration = pulse_end - pulse_start
        return (duration * 34300) / 2  # cm
    
    def thread_function(self):
        while True:
            dist = self.measure_distance()
            if dist:
                self.distance = dist
            time.sleep(0.01)  # Ajustar el tiempo de espera según sea necesario