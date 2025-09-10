from utils.i2c_manager import i2c
import adafruit_vl53l0x
import libs.GPIO as GPIO
import time

class DistanceSensor:
    def __init__(self, xshut_pin, new_address=0x29):
        self.xshut = xshut_pin
        self.address = new_address

        # Configura XSHUT
        GPIO.setup(self.xshut, GPIO.OUT)
        GPIO.output(self.xshut, GPIO.LOW)   # Apagado
        time.sleep(0.01)
        
    def init_sensor(self):
        # Enciende
        GPIO.output(self.xshut, GPIO.HIGH)
        time.sleep(0.05)

        # Inicializa con dirección por defecto
        sensor = adafruit_vl53l0x.VL53L0X(i2c)

        # Cambia dirección
        sensor.set_address(self.address)
        self.sensor = sensor

    def get_distance(self):
        return self.sensor.range