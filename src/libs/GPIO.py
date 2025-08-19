import lgpio
import threading
import time

OUT = 0
IN = 1

# Abrir chip principal raspberry
chip = lgpio.gpiochip_open(0)

# funciones basicas
def setup(pin, mode):
    if mode == OUT:
        lgpio.gpio_claim_output(chip, pin)
    elif mode == IN:
        lgpio.gpio_claim_input(chip, pin)
    else:
        raise ValueError("Modo no soportado")

def output(pin, value):
    lgpio.gpio_write(chip, pin, value)

def input(pin):
    return lgpio.gpio_read(chip, pin)

class PWM:
    def __init__(self, pin, frequency=1000):
        self.chip = chip
        self.pin = pin
        self.freq = frequency
        self.duty = 0
        self.running = False
        self.thread = None
    
    def start(self, duty_cycle):
        self.duty = duty_cycle
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def _run(self):
        period = 1.0 / self.freq 
        while self.running:
            high_time = period * (self.duty / 100.0)
            low_time = period - high_time
            if self.duty > 0:
                lgpio.gpio_write(self.chip, self.pin, 1)
                time.sleep(high_time)
            if self.duty < 100:
                lgpio.gpio_write(self.chip, self.pin, 0)
                time.sleep(low_time)
    def ChangeDutyCycle(self, duty_cycle):
        self.duty = duty_cycle
    
    def stop(self):
        self.running = False
        lgpio.gpio_write(self.chip, self.pin, 0)
    
def cleanup():
    lgpio.gpiochip_close(chip)