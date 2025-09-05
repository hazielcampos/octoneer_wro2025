import smbus
import time

# Dirección I2C del MPU6050
MPU6050_ADDR = 0x68

# Registros del MPU6050
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Inicializar I2C
bus = smbus.SMBus(1)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)  # Despertar el sensor

def read_word(reg):
    high = bus.read_byte_data(MPU6050_ADDR, reg)
    low = bus.read_byte_data(MPU6050_ADDR, reg+1)
    value = (high << 8) + low
    if value >= 0x8000:
        value = -((65535 - value) + 1)
    return value

def get_accel_gyro():
    accel_x = read_word(ACCEL_XOUT_H) / 16384.0
    accel_y = read_word(ACCEL_XOUT_H+2) / 16384.0
    accel_z = read_word(ACCEL_XOUT_H+4) / 16384.0

    gyro_x = read_word(GYRO_XOUT_H) / 131.0
    gyro_y = read_word(GYRO_XOUT_H+2) / 131.0
    gyro_z = read_word(GYRO_XOUT_H+4) / 131.0

    return {
        "accel": (accel_x, accel_y, accel_z),
        "gyro": (gyro_x, gyro_y, gyro_z)
    }

while True:
    data = get_accel_gyro()
    print("Accel:", data["accel"], " Gyro:", data["gyro"])
    time.sleep(0.5)
