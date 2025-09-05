import smbus
import time
import math
import tkinter as tk

# Dirección I2C del MPU6050
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_ZOUT_H = 0x47

bus = smbus.SMBus(1)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def read_word(reg):
    high = bus.read_byte_data(MPU6050_ADDR, reg)
    low = bus.read_byte_data(MPU6050_ADDR, reg+1)
    value = (high << 8) + low
    if value >= 0x8000:
        value = -((65535 - value) + 1)
    return value

def get_gyro_z():
    gz = read_word(GYRO_ZOUT_H) / 131.0
    return gz

# -------------------------------
# Yaw relativo
# -------------------------------
dt = 0.05  # intervalo (50ms)
yaw = 0.0
yaw_offset = 0.0

def update_yaw():
    global yaw
    gz = get_gyro_z()
    yaw += gz * dt  # integración
    return (yaw - yaw_offset) % 360  # mantener en [0-360)

def reset_yaw():
    global yaw_offset
    yaw_offset = yaw

# -------------------------------
# Tkinter GUI
# -------------------------------
root = tk.Tk()
root.title("MPU6050 - Yaw (Rotación Z)")

canvas = tk.Canvas(root, width=400, height=400, bg="black")
canvas.grid(row=0, column=0, rowspan=3)

label_yaw = tk.Label(root, text="Yaw: 0°", font=("Arial", 16))
label_yaw.grid(row=0, column=1, sticky="w", padx=10)

btn_reset = tk.Button(root, text="Reset Yaw", font=("Arial", 14), command=reset_yaw)
btn_reset.grid(row=1, column=1, sticky="w", padx=10)

def draw_arrow(angle):
    canvas.delete("all")

    cx, cy = 200, 200
    length = 100

    rad = math.radians(angle)
    x_end = cx + length * math.cos(rad)
    y_end = cy - length * math.sin(rad)

    # Flecha
    canvas.create_line(cx, cy, x_end, y_end, fill="red", width=4, arrow=tk.LAST)
    canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill="white")

def update():
    current_yaw = update_yaw()
    draw_arrow(current_yaw)

    # Mostrar ángulo en grados
    label_yaw.config(text=f"Yaw: {current_yaw:.1f}°")

    root.after(int(dt*1000), update)

update()
root.mainloop()
