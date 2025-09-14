import cv2

lower_1 = (107, 46, 63)
upper_1 = (130, 129, 148)

lower_2 = (0, 76, 24)
upper_2 = (45, 124, 113)

x1, x2 = 200, 400
y1, y2 = 400, 480

last_callback = 0
def trigger_line(running, hsv, frame, callback_1, callback_2):
    global last_callback
    roi = hsv[y1:y2, x1:x2]
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    mask_1 = cv2.inRange(roi, lower_1, upper_1)
    mask_2 = cv2.inRange(roi, lower_2, upper_2)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, kernel)
    mask_2 = cv2.morphologyEx(mask_2, cv2.MORPH_OPEN, kernel)
    cv2.imshow("Mask 1", mask_1)
    cv2.imshow("Mask 2", mask_2)
    
    count_1 = cv2.countNonZero(mask_1)
    count_2 = cv2.countNonZero(mask_2)
    
    if count_1 > 200:
        print("Azul detectado")
        if not running:
            return
        if callback_1 and last_callback != 1:
            callback_1()
        last_callback = 1
    elif count_2 > 200:
        print("Naranja detectado")
        if not running:
            return
        if callback_2 and last_callback != 2:
            callback_2()
        last_callback = 2
        
def invert_last_callback():
    global last_callback
    last_callback = 1 if last_callback == 2 else 2
