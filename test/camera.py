import cv2
import numpy as np

def nothing(x):
    pass

# Abrir cámara
cap = cv2.VideoCapture(0)

# Crear ventana con sliders
cv2.namedWindow("Trackbars")

# Sliders para el valor central
cv2.createTrackbar("H", "Trackbars", 90, 179, nothing)   # tono
cv2.createTrackbar("S", "Trackbars", 150, 255, nothing)  # saturación
cv2.createTrackbar("V", "Trackbars", 150, 255, nothing)  # brillo

# Sliders para tolerancias (margen alrededor del valor central)
cv2.createTrackbar("Tol H", "Trackbars", 10, 50, nothing)
cv2.createTrackbar("Tol S", "Trackbars", 50, 127, nothing)
cv2.createTrackbar("Tol V", "Trackbars", 50, 127, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Leer valores de los sliders
    h = cv2.getTrackbarPos("H", "Trackbars")
    s = cv2.getTrackbarPos("S", "Trackbars")
    v = cv2.getTrackbarPos("V", "Trackbars")

    tol_h = cv2.getTrackbarPos("Tol H", "Trackbars")
    tol_s = cv2.getTrackbarPos("Tol S", "Trackbars")
    tol_v = cv2.getTrackbarPos("Tol V", "Trackbars")

    # Generar umbrales dinámicamente
    lower = (max(0, h - tol_h), max(0, s - tol_s), max(0, v - tol_v))
    upper = (min(179, h + tol_h), min(255, s + tol_s), min(255, v + tol_v))

    # Crear máscara
    mask = cv2.inRange(hsv, lower, upper)

    # Mostrar resultados
    cv2.imshow("Original", frame)
    cv2.imshow("Mask", mask)

    # Imprimir rangos actuales
    print(f"Lower: {lower}, Upper: {upper}", end="\r")

    if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
