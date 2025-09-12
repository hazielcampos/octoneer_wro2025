import cv2

lower_1 = (151, 71, 88)
upper_1 = (179, 195, 190)

lower_2 = (88, 74, 43)
upper_2 = (136, 175, 134)

x1, x2 = 200, 400
y1, y2 = 400, 480

def trigger_line(hsv, frame):
    roi = hsv[y1:y2, x1:x2]
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    mask_1 = cv2.inRange(roi, lower_1, upper_1)
    mask_2 = cv2.inRange(roi, lower_2, upper_2)
    cv2.imshow("Mask 1", mask_1)
    cv2.imshow("Mask 2", mask_2)
    
    count_1 = cv2.countNonZero(mask_1)
    count_2 = cv2.countNonZero(mask_2)
    
    if count_1 > 500:
        cv2.putText(frame, "Mask 1 Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    elif count_2 > 500:
        cv2.putText(frame, "Mask 2 Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    else:
        cv2.putText(frame, "None Mask Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        