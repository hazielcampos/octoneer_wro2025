import Rasp.GPIO as GPIO
import time
import threading

class HCSR04:
    def __init__(self, echo, trigger):
        self.echo = echo
        self.trigger = trigger
        self.distance = 0.0
        self.thread = threading.Thread(target=self.thread_function, daemon=True)
        
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.output(self.trigger, False)
        
        time.sleep(0.0002)
        
        self.thread.start()
    
    def get_distance(self, timeout=0.02):
        GPIO.output(self.trigger, False)
        time.sleep(0.000002)
        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
        
        start_time = time.time()
        
        while GPIO.input(self.echo) == 0:
            if time.time() - start_time > timeout:
                return None
        
        pulse_start = time.time()
        
        while GPIO.input(self.echo) == 1:
            if time.time() - pulse_start > timeout:
                return None
            
        pulse_end = time.time()
        
        duration = pulse_end - pulse_start
        return (duration * 34300) / 2
    
    def thread_function(self):
        try:
            while True:
                dist = self.get_distance()
                if dist:
                    self.distance = dist
                
                time.sleep(0.01)
        finally:
            print("[WARNING] Ultrasonic sensor terminated.")