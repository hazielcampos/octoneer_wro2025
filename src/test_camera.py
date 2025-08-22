import cv2
import numpy as np

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    
    if not ret:
        break
    cv2.imshow('Camera Feed', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
