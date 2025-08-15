import RPi.GPIO as GPIO

class Motor:
    def __init__(self, pin_forward, pin_backward):
        self.pin_forward = pin_forward
        self.pin_backward = pin_backward
        GPIO.setup(self.pin_forward, GPIO.OUT)
        GPIO.setup(self.pin_backward, GPIO.OUT)
        self.pwm_forward = GPIO.PWM(self.pin_forward, 100)
        self.pwm_backward = GPIO.PWM(self.pin_backward, 100)
        self.pwm_forward.start(0)
        self.pwm_backward.start(0)
    
    def forward(self, speed=1.0):
        self.pwm_forward.ChangeDutyCycle(speed * 100)
        self.pwm_backward.ChangeDutyCycle(0)
    def backward(self, speed=1.0):
        self.pwm_backward.ChangeDutyCycle(speed * 100)
        self.pwm_forward.ChangeDutyCycle(0)
    def stop(self):
        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(0)