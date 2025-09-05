import smbus
import time
import math
import tkinter as tk

# Dirección I2C del MPU6050
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

bus = smbus.SMBus(1)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

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

    return accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z

# -------------------------------
# Filtro complementario
# -------------------------------
dt = 0.05  # intervalo (50ms)
alpha = 0.98  # peso del giroscopio

pitch, roll, yaw = 0.0, 0.0, 0.0

def update_orientation():
    global pitch, roll, yaw

    ax, ay, az, gx, gy, gz = get_accel_gyro()

    # Ángulos desde acelerómetro
    accel_pitch = math.degrees(math.atan2(ay, math.sqrt(ax*ax + az*az)))
    accel_roll = math.degrees(math.atan2(-ax, az))

    # Integración del giroscopio
    pitch += gx * dt
    roll += gy * dt
    yaw += gz * dt  # ⚠️ sin magnetómetro se deriva

    # Filtro complementario (solo para pitch y roll)
    pitch = alpha * pitch + (1 - alpha) * accel_pitch
    roll = alpha * roll + (1 - alpha) * accel_roll

    return pitch, roll, yaw

# -------------------------------
# Tkinter GUI
# -------------------------------
root = tk.Tk()
root.title("MPU6050 - Orientación Robot")

canvas = tk.Canvas(root, width=400, height=400, bg="black")
canvas.grid(row=0, column=0, rowspan=4)

label_pitch = tk.Label(root, text="Pitch: 0°", font=("Arial", 14))
label_pitch.grid(row=0, column=1, sticky="w")

label_roll = tk.Label(root, text="Roll: 0°", font=("Arial", 14))
label_roll.grid(row=1, column=1, sticky="w")

label_yaw = tk.Label(root, text="Yaw: 0°", font=("Arial", 14))
label_yaw.grid(row=2, column=1, sticky="w")

def draw_horizon(pitch, roll):
    canvas.delete("all")

    # Centro del canvas
    cx, cy = 200, 200

    # Rectángulo que simula el horizonte
    size = 300
    x1, y1 = -size, 0
    x2, y2 = size, 0
    x3, y3 = size, size
    x4, y4 = -size, size

    # Rotar por roll
    angle = math.radians(roll)
    cos_a, sin_a = math.cos(angle), math.sin(angle)

    points = []
    for x, y in [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]:
        xr = x * cos_a - y * sin_a
        yr = x * sin_a + y * cos_a
        points.append(cx + xr)
        points.append(cy + yr + pitch*2)  # desplazar vertical por pitch

    # Dibujar tierra (marrón)
    canvas.create_polygon(points, fill="sienna", outline="")
    # Dibujar cielo (azul)
    canvas.create_polygon(points[0:4] + [points[6], points[7], points[0], points[1]], fill="skyblue", outline="")

    # Línea del horizonte
    canvas.create_line(points[0], points[1], points[2], points[3], fill="white", width=3)

    # Cruz central
    canvas.create_line(cx-20, cy, cx+20, cy, fill="white", width=2)
    canvas.create_line(cx, cy-20, cx, cy+20, fill="white", width=2)

def update():
    pitch, roll, yaw = update_orientation()
    draw_horizon(pitch, roll)

    # Actualizar etiquetas
    label_pitch.config(text=f"Pitch: {pitch:.1f}°")
    label_roll.config(text=f"Roll: {roll:.1f}°")
    label_yaw.config(text=f"Yaw: {yaw:.1f}°")

    root.after(int(dt*1000), update)

update()
root.mainloop()
