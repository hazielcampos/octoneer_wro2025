# mpu_yaw_gui_calibrado.py
# Requisitos: python3, python3-smbus, tkinter
# Conecta MPU6050 (SDA,SCL,VCC(3.3V),GND) y habilita I2C.

import smbus
import time
import math
import tkinter as tk

# ----- Config MPU6050 -----
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_ZOUT_H = 0x47
ACCEL_XOUT_H = 0x3B

bus = smbus.SMBus(1)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)  # wake up

def read_word(reg):
    high = bus.read_byte_data(MPU6050_ADDR, reg)
    low = bus.read_byte_data(MPU6050_ADDR, reg+1)
    val = (high << 8) + low
    if val >= 0x8000:
        val = -((65535 - val) + 1)
    return val

def get_gyro_z_raw():
    return read_word(GYRO_ZOUT_H)

def get_accel_raw():
    ax = read_word(ACCEL_XOUT_H)
    ay = read_word(ACCEL_XOUT_H+2)
    az = read_word(ACCEL_XOUT_H+4)
    return ax, ay, az

def gyro_raw_to_dps(raw):
    # Sensibilidad por defecto ±250 °/s -> 131 LSB/(°/s)
    return raw / 131.0

def accel_raw_to_g(raw):
    # Sensibilidad por defecto ±2g -> 16384 LSB/g
    return raw / 16384.0

# ----- Parámetros -----
AUTO_CAL_SECONDS = 2.0    # tiempo para calibración inicial (s)
AUTO_CAL_SAMPLES = 200
STATIONARY_GYRO_THRESH = 1.0   # °/s - si gz bajo => quieto
STATIONARY_ACCEL_THRESH = 0.05 # g - variación pequeña en aceleración
STATIONARY_REQUIRED_SECONDS = 2.0  # tiempo continuo para considerar quieto

# estado
yaw = 0.0                # ángulo integrado (°)
yaw_offset = 0.0         # offset para reset/zero
gyro_z_bias = 0.0        # bias estimado (°/s)
last_time = None

# buffer para detección quieto
stationary_start = None

# ----- Calibración inicial de bias -----
def calibrate_gyro_z(samples=AUTO_CAL_SAMPLES, delay=0.005):
    print("Calibrando gyro z... mantén el robot quieto.")
    s = 0.0
    for i in range(samples):
        raw = get_gyro_z_raw()
        dps = gyro_raw_to_dps(raw)
        s += dps
        time.sleep(delay)
    bias = s / samples
    print(f"Bias inicial estimado: {bias:.4f} °/s")
    return bias

# ----- Auto-recalibración cuando el robot está quieto -----
def is_stationary(gz_dps, ax, ay, az):
    # gz pequeño y aceleración cerca de 1g (sin movimientos)
    g_mag = math.sqrt(ax*ax + ay*ay + az*az)
    accel_diff = abs(g_mag - 1.0)
    return (abs(gz_dps) < STATIONARY_GYRO_THRESH) and (accel_diff < STATIONARY_ACCEL_THRESH)

def try_auto_recalibrate(gz_dps, ax, ay, az):
    global stationary_start, gyro_z_bias
    t = time.time()
    if is_stationary(gz_dps, ax, ay, az):
        if stationary_start is None:
            stationary_start = t
        elif (t - stationary_start) >= STATIONARY_REQUIRED_SECONDS:
            # recalibrar bias tomando N muestras
            print("Robot quieto: recalibrando bias gyro z automáticamente...")
            gyro_z_bias = calibrate_gyro_z(samples=200, delay=0.003)
            stationary_start = None
    else:
        stationary_start = None

# ----- Reset manual del yaw -----
def reset_yaw():
    global yaw_offset, yaw
    yaw_offset = yaw
    print("Yaw reseteado (offset actualizado).")

# ----- GUI y loop principal -----
dt_min = 0.002  # evitar dt=0

def update_once():
    global yaw, last_time

    now = time.time()
    if last_time is None:
        last_time = now
    dt = now - last_time
    if dt < dt_min:
        dt = dt_min
    last_time = now

    # leer raw
    gz_raw = get_gyro_z_raw()
    ax_raw, ay_raw, az_raw = get_accel_raw()

    # convertir a unidades físicas
    gz = gyro_raw_to_dps(gz_raw)  # °/s
    ax = accel_raw_to_g(ax_raw)
    ay = accel_raw_to_g(ay_raw)
    az = accel_raw_to_g(az_raw)

    # intentar recalibración automática si está quieto
    try_auto_recalibrate(gz, ax, ay, az)

    # corregir bias
    gz_corr = gz - gyro_z_bias

    # integrar yaw
    yaw += gz_corr * dt  # grados

    # normalizar entre 0-360
    yaw_display = ((yaw - yaw_offset) % 360.0 + 360.0) % 360.0

    # actualizar GUI
    label_yaw.config(text=f"Yaw: {yaw_display:.1f}°")
    # actualizar flecha
    draw_arrow(yaw_display)

    # programar siguiente iteración
    root.after(10, update_once)  # ~100 Hz intentado; control real via dt

# ----- Dibujo de flecha -----
def draw_arrow(angle_deg):
    canvas.delete("all")
    cx, cy = 200, 200
    length = 120
    rad = math.radians(angle_deg)
    x_end = cx + length * math.cos(rad)
    y_end = cy - length * math.sin(rad)
    canvas.create_oval(cx-6, cy-6, cx+6, cy+6, fill="white")
    canvas.create_line(cx, cy, x_end, y_end, fill="lime", width=4, arrow=tk.LAST)
    # marcas cada 45°
    for a in range(0, 360, 45):
        r = math.radians(a)
        x = cx + (length+18) * math.cos(r)
        y = cy - (length+18) * math.sin(r)
        canvas.create_text(x, y, text=str(a), fill="white", font=("Arial", 9))

# ----- Setup GUI -----
root = tk.Tk()
root.title("MPU6050 - Yaw (calibrado + auto-recal)")

canvas = tk.Canvas(root, width=400, height=400, bg="black")
canvas.grid(row=0, column=0, rowspan=4)

label_yaw = tk.Label(root, text="Yaw: 0°", font=("Arial", 16))
label_yaw.grid(row=0, column=1, sticky="w", padx=10, pady=6)

btn_reset = tk.Button(root, text="Reset Yaw", font=("Arial", 14), command=reset_yaw)
btn_reset.grid(row=1, column=1, sticky="w", padx=10)

lbl_info = tk.Label(root, text="Estado: calibrando...", font=("Arial", 10))
lbl_info.grid(row=2, column=1, sticky="w", padx=10)

# ----- Inicio: calibración inicial -----
gyro_z_bias = calibrate_gyro_z(samples=AUTO_CAL_SAMPLES, delay=AUTO_CAL_SECONDS / AUTO_CAL_SAMPLES)
lbl_info.config(text=f"Bias inicial: {gyro_z_bias:.4f} °/s  (auto-recal cuando esté quieto)")

# empezar loop
last_time = None
root.after(50, update_once)
root.mainloop()
