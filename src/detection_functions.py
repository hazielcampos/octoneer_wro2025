import cv2
import numpy as np

naranja_hsv = (0, 97, 112)
naranja_tol = (27, 35, 69)

azul_hsv = (118, 77, 92)
azul_tol = (22, 60, 79)

MIN_AREA = 20

x1, x2 = 250, 350
y1, y2 = 400, 440

def get_mask(roi, color_hsv, tol_hsv):
    h, s, v = color_hsv
    tol_h, tol_s, tol_v = tol_hsv
    
    lower = (max(0, h - tol_h), max(0, s - tol_s), max(0, v - tol_v))
    upper = (min(179, h + tol_h), min(255, s + tol_s), min(255, v + tol_v))
    
    mask = cv2.inRange(roi, lower, upper)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    clean_mask = np.zeros_like(mask)
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area >= MIN_AREA:
            clean_mask[labels == i] = 255
            
    return clean_mask
    

last_callback = 0
def trigger_line(running, hsv, frame, callback_1, callback_2):
    global last_callback
    roi = hsv[y1:y2, x1:x2]
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    mask_1 = get_mask(roi, azul_hsv, azul_tol)
    mask_2 = get_mask(roi, naranja_hsv, naranja_tol)
    
    count_1 = cv2.countNonZero(mask_1)
    count_2 = cv2.countNonZero(mask_2)
    
    if count_1 > MIN_AREA:
        if not running:
            return
        if callback_1 and last_callback != 1:
            print("Azul detectado")
            callback_1()
        last_callback = 1
    elif count_2 > MIN_AREA:
        if not running:
            return
        if callback_2 and last_callback != 2:
            print("Naranja detectado")
            callback_2()
        last_callback = 2
        
def invert_last_callback():
    global last_callback
    last_callback = 1 if last_callback == 2 else 2
