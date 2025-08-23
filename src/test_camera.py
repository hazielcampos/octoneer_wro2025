import cv2
import numpy as np

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    
    if not ret:
        break
    
    cv2.rectangle(frame, (0, 0), (640, 220), (0, 255, 0), 2)
    cv2.rectangle(frame, (0, 0), (214, 220), (255, 0, 0), 2)
    cv2.rectangle(frame, (214, 0), (428, 220), (0, 0, 255), 2)
    cv2.rectangle(frame, (428, 0), (640, 220), (255, 255, 0), 2)
    cv2.imshow('Camera Feed', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
