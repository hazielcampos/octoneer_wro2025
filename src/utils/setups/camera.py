import cv2
import numpy as np

def nothing(x):
    pass

# Cargar imagen o video
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# Crear ventana
cv2.namedWindow("Trackbars")

# Crear sliders para espacio LAB
cv2.createTrackbar("L_lower", "Trackbars", 0, 100, nothing)    # Luminance: 0-100
cv2.createTrackbar("L_upper", "Trackbars", 100, 100, nothing)  # Luminance: 0-100
cv2.createTrackbar("A_lower", "Trackbars", 0, 255, nothing)    # A: -128 to +127 (offset +128)
cv2.createTrackbar("A_upper", "Trackbars", 255, 255, nothing)  # A: -128 to +127 (offset +128)
cv2.createTrackbar("B_lower", "Trackbars", 0, 255, nothing)    # B: -128 to +127 (offset +128)
cv2.createTrackbar("B_upper", "Trackbars", 255, 255, nothing)  # B: -128 to +127 (offset +128)

while True:
    _, frame = cap.read()
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)  # Convertir a LAB en lugar de HSV

    # Leer valores de los sliders
    ll = cv2.getTrackbarPos("L_lower", "Trackbars")
    ul = cv2.getTrackbarPos("L_upper", "Trackbars")
    la = cv2.getTrackbarPos("A_lower", "Trackbars")
    ua = cv2.getTrackbarPos("A_upper", "Trackbars")
    lb = cv2.getTrackbarPos("B_lower", "Trackbars")
    ub = cv2.getTrackbarPos("B_upper", "Trackbars")

    # Crear arrays para los límites
    lower = np.array([ll, la, lb])
    upper = np.array([ul, ua, ub])

    mask = cv2.inRange(lab, lower, upper)  # Aplicar máscara al espacio LAB
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    if cv2.waitKey(1) & 0xFF == 27: # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()