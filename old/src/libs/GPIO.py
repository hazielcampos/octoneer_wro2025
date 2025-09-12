import lgpio
import threading
import time

OUT = 0
IN = 1

PUD_OFF = None
PUD_DOWN = lgpio.SET_PULL_DOWN
PUD_UP   = lgpio.SET_PULL_UP
LOW = 0
HIGH = 1

# Open the GPIO chip (usually chip 0 for Raspberry Pi)
chip = lgpio.gpiochip_open(0)
active_pwm = []

# Basic GPIO functions
def setup(pin, mode, pull_up_down=PUD_OFF):
    if mode == OUT:
        lgpio.gpio_claim_output(chip, pin)
    elif mode == IN:
        if pull_up_down == PUD_OFF:
            lgpio.gpio_claim_input(chip, pin)
        else:
            lgpio.gpio_claim_input(chip, pin, pull_up_down)
    else:
        raise ValueError("Modo no soportado")

def output(pin, value):
    lgpio.gpio_write(chip, pin, value)

def input(pin):
    return lgpio.gpio_read(chip, pin)

class PWM:
    def __init__(self, pin, frequency=1000):
        self.lock = threading.Lock()
        self.chip = chip
        self.pin = pin
        self.freq = frequency
        self.duty = 0
        self.running = False
        self.thread = None
        active_pwm.append(self)
    
    def __del__(self):
        self.stop()
        if self in active_pwm:
            active_pwm.remove(self)
    
    def start(self, duty_cycle):
        if self.running:
            return
        self.duty = max(0, min(100, duty_cycle))
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def _run(self):
        try:
            period = 1.0 / self.freq 
            while self.running:
                with self.lock:
                    duty = self.duty
                high_time = period * (duty / 100.0)
                low_time = period - high_time
                if duty > 0:
                    lgpio.gpio_write(self.chip, self.pin, 1)
                    time.sleep(high_time)
                if duty < 100:
                    lgpio.gpio_write(self.chip, self.pin, 0)
                    time.sleep(low_time)
        except Exception as e:
            print(f"Error in PWM thread: {e}")
            lgpio.gpio_write(self.chip, self.pin, 0)
        finally:
            lgpio.gpio_write(self.chip, self.pin, 0)
            
    def ChangeDutyCycle(self, duty_cycle):
        with self.lock:
            self.duty = max(0, min(100, duty_cycle))
            
    def stop(self):
        self.running = False
        lgpio.gpio_write(self.chip, self.pin, 0)
    
def cleanup():
    for pwm in active_pwm:
        pwm.stop()
    lgpio.gpiochip_close(chip)
    