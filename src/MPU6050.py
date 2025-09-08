import smbus
import time
import math
import threading

class MPU6050:
    def __init__(self, auto_calibrate = False):
        self.ADDR = 0x68
        self.PWR_MGMT_1 = 0x6B
        self.GYRO_ZOUT_H = 0x47
        self.ACCEL_XOUT_H = 0x3B
        
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(self.ADDR, self.PWR_MGMT_1, 0)
        
        self.AUTO_CAL_SECONDS = 2.0
        self.AUTO_CAL_SAMPLES = 200
        self.STATIONARY_GYRO_THRESH = 1.0
        self.STATIONARY_ACCEL_THRESH = 0.05
        self.STATIONARY_REQUIRED_SECONDS = 2.0
        
        self.yaw = 0.0
        self.yaw_offset = 0.0
        self.gyro_z_bias = 0.0
        self.last_time = None
        self.dt_min = 0.002
        
        self.stationary_start = None
        
        self.sensor_thread = threading.Thread(daemon=True, target=self.update_loop)
        self.auto_calibrate = auto_calibrate
    
    def start(self):
        self.sensor_thread.start()
        
    def read_word(self, reg):
        high = self.bus.read_byte_data(self.ADDR, reg)
        low = self.bus.read_byte_data(self.ADDR, reg+1)
        val = (high << 8) + low
        if val >> 0x8000:
            val = -((65535 - val) + 1)
        return val

    def get_gyro_z_raw(self):
        return self.read_word(self.GYRO_ZOUT_H)
    
    def get_accel_raw(self):
        ax = self.read_word(self.ACCEL_XOUT_H)
        ay = self.read_word(self.ACCEL_XOUT_H+2)
        az = self.read_word(self.ACCEL_XOUT_H+4)
        return ax, ay, az
    
    def gyro_raw_to_dps(self, raw):
        return raw / 131.0
    
    def accel_raw_to_g(self, raw):
        return raw / 16384.0
    
    def calibrate_gyro_z(self, samples = 0, delay=0.005):
        if samples == 0:
            samples = self.AUTO_CAL_SAMPLES
        print("Calibrando gyro z... manten el robot quieto...")
        s = 0.0
        for i in range(samples):
            raw = self.get_gyro_z_raw()
            dps = self.gyro_raw_to_dps(raw)
            s += dps
            time.sleep(delay)
        
        bias = s / samples
        print(f"Bias inicial estimado: {bias:.4f}")
        return bias

    def is_stationary(self, gz_dps, ax, ay, az):
        g_mag = math.sqrt(ax*ax + ay*ay + az*az)
        accel_diff = abs(g_mag - 1.0)
        return (abs(gz_dps) < self.STATIONARY_GYRO_THRESH) and (accel_diff < self.STATIONARY_ACCEL_THRESH)
    
    def try_auto_recalibrate(self,gz_dps, ax, ay, az):
        t = time.time()
        if self.is_stationary(gz_dps, ax, ay, az):
            if self.stationary_start is None:
                self.stationary_start = t
            elif (t - self.stationary_start) >= self.STATIONARY_REQUIRED_SECONDS:
                print("Robot quieto: recalibrando bias gyro z automáticamente...")
                self.gyro_z_bias = self.calibrate_gyro_z(samples=200, delay=0.003)
                self.stationary_start = None
            else:
                self.stationary_start = None
    def reset_yaw(self):
        self.yaw_offset = self.yaw
        print("Yaw reseteado (offset actualizado)")
        
    def get_yaw(self):
        return ((self.yaw - self.yaw_offset) % 360.0 + 360.0) % 360.0
    
    def update(self):
        now = time.time()
        if self.last_time is None:
            self.last_time = now
        dt = now - self.last_time
        if dt < self.dt_min:
            dt = self.dt_min
        self.last_time = now
        
        gz_raw = self.get_gyro_z_raw()
        ax_raw, ay_raw, az_raw = self.get_accel_raw()
        
        gz = self.gyro_raw_to_dps(gz_raw)
        ax = self.accel_raw_to_g(ax_raw)
        ay = self.accel_raw_to_g(ay_raw)
        az = self.accel_raw_to_g(az_raw)
        
        if self.auto_calibrate:
            self.try_auto_recalibrate(gz, ax, ay, az)
        
        gz_corr = gz - self.gyro_z_bias
        
        self.yaw += gz_corr * dt
    def update_loop(self):
        self.gyro_z_bias = self.calibrate_gyro_z(samples=200, delay=0.003)
        while True:
            self.update()
            time.sleep(0.002)