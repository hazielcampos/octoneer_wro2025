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

# Crear sliders
cv2.createTrackbar("LH", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("LS", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("LV", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("UH", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("US", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("UV", "Trackbars", 255, 255, nothing)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Leer valores de los sliders
    ll = cv2.getTrackbarPos("L_lower", "Trackbars")
    ul = cv2.getTrackbarPos("L_upper", "Trackbars")
    la = cv2.getTrackbarPos("A_lower", "Trackbars")
    ua = cv2.getTrackbarPos("A_upper", "Trackbars")
    lb = cv2.getTrackbarPos("B_lower", "Trackbars")
    ub = cv2.getTrackbarPos("B_upper", "Trackbars")

    lower = np.array([ll, la, lb])
    upper = np.array([ul, ua, ub])

    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    if cv2.waitKey(1) & 0xFF == 27: # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
