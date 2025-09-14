"""
valores de naranja
h = 0
s = 97
v = 112

tol_h = 17
tol_s = 25
tol_v = 69

"""

"""
valores de azul

h 118
s 77
v 92

tol_h 12
tol_s 50
tol_v 79
"""

"""
valores verde
h 80
s 109
v 91

tol_h 21
tol_s 44
tol_v 48
"""

"""
valores rojo

h 179
s 133
v 141

tol_h 15 
tol_s 72
tol_v 120
"""
import cv2
import numpy as np

def nothing(x): pass

cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")

cv2.createTrackbar("H", "Trackbars", 90, 179, nothing)
cv2.createTrackbar("S", "Trackbars", 150, 255, nothing)
cv2.createTrackbar("V", "Trackbars", 150, 255, nothing)
cv2.createTrackbar("Tol H", "Trackbars", 10, 50, nothing)
cv2.createTrackbar("Tol S", "Trackbars", 50, 127, nothing)
cv2.createTrackbar("Tol V", "Trackbars", 50, 127, nothing)

MIN_AREA = 500

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h = cv2.getTrackbarPos("H", "Trackbars")
    s = cv2.getTrackbarPos("S", "Trackbars")
    v = cv2.getTrackbarPos("V", "Trackbars")

    tol_h = cv2.getTrackbarPos("Tol H", "Trackbars")
    tol_s = cv2.getTrackbarPos("Tol S", "Trackbars")
    tol_v = cv2.getTrackbarPos("Tol V", "Trackbars")

    lower = (max(0, h - tol_h), max(0, s - tol_s), max(0, v - tol_v))
    upper = (min(179, h + tol_h), min(255, s + tol_s), min(255, v + tol_v))

    mask = cv2.inRange(hsv, lower, upper)

    # Morfología inicial
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # 🔥 Fusionar blobs cercanos (dilatación ligera)
    kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    mask = cv2.dilate(mask, kernel_dilate, iterations=1)

    # Eliminar blobs pequeños después de unir
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    clean_mask = np.zeros_like(mask)

    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area >= MIN_AREA:
            clean_mask[labels == i] = 255

    cv2.imshow("Original", frame)
    cv2.imshow("Mask", clean_mask)

    print(f"Lower: {lower}, Upper: {upper}", end="\r")

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
