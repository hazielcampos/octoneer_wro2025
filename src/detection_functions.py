import cv2

lower_1 = (100, 38, 84)
upper_1 = (123, 117, 137)

lower_2 = (0, 60, 137)
upper_2 = (32, 151, 224)

x1, x2 = 200, 400
y1, y2 = 400, 480

last_callback = 1
def trigger_line(hsv, frame, callback_1, callback_2):
    global last_callback
    roi = hsv[y1:y2, x1:x2]
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    mask_1 = cv2.inRange(roi, lower_1, upper_1)
    mask_2 = cv2.inRange(roi, lower_2, upper_2)
    cv2.imshow("Mask 1", mask_1)
    cv2.imshow("Mask 2", mask_2)
    
    count_1 = cv2.countNonZero(mask_1)
    count_2 = cv2.countNonZero(mask_2)
    
    if count_1 > 500 and last_callback != 1:
        cv2.putText(frame, "Mask 1 Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        if callback_1:
            callback_1()
        last_callback = 1
    elif count_2 > 500 and last_callback != 2:
        cv2.putText(frame, "Mask 2 Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        if callback_2:
            callback_2()
        last_callback = 2
    else:
        cv2.putText(frame, "None Mask Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        
def invert_last_callback():
    global last_callback
    last_callback = 1 if last_callback == 2 else 2
