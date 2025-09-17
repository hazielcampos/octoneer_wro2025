import numpy as np
import cv2 
import time
from collections import deque
import threading
from enums.enums import Color
lock = threading.Lock()
import masks as Mask

class ObstacleClasifier:
    def __init__(self, roi=((0, 0), (320, 240))):
        self.thread = threading.Thread(target=self.main)
        self.kernel = np.ones((3, 3), "uint8")
        self.history = deque(maxlen=10)
        self.frame = np.zeros((320, 240, 3), "uint8")
        self.roi = roi
        
        self.lower_red = (134, 130, 21)
        self.upper_red = (179, 190, 152)
        
        self.lower_green = (51, 72, 5)
        self.upper_green = (74, 152, 59)
        self.obstacle = None
        self.end_thread = False
        self.display_frame = np.zeros((320, 240, 3), "uint8")
        self.last_frame_time = time.time()
        self.fps = 0
        
    def start(self):
        self.thread.start()
        
    def set_frame(self, frame):
        with lock:
            now = time.time()
            self.fps = 1 / max(now - self.last_frame_time, 1e-6)  # FPS basado en la cámara
            self.last_frame_time = now
            self.frame = frame
        
    def main(self):
        while not self.end_thread:
            with lock:
                imageFrame = self.frame.copy()
            lab = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2LAB)
            
            red_mask = cv2.inRange(lab, Mask.lower_red, Mask.upper_red)
            green_mask = cv2.inRange(lab, Mask.lower_green, Mask.upper_green)
            
            red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, self.kernel)
            red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, self.kernel)
            
            green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, self.kernel)
            green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, self.kernel)
            
            contours_red, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours_green, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            detected_objects = []
            
            for contour in contours_red:
                area = cv2.contourArea(contour)
                if area > 1000:
                    x, y, w, h = cv2.boundingRect(contour)
                    detected_objects.append((area, (x, y, w, h), Color.RED, (0, 0, 255)))
            for contour in contours_green:
                area = cv2.contourArea(contour)
                if area > 1000:
                    x, y, w, h = cv2.boundingRect(contour)
                    detected_objects.append((area, (x, y, w, h), Color.GREEN, (0, 255, 0)))
            
            if self.roi:
                (x1, y1), (x2, y2) = self.roi
                def inside_roi(obj):
                    _, (x, y, w, h), _, _ = obj
                    cx = x + w // 2
                    cy = y + h // 2
                    return x1 <= cx <= x2 and y1 <= cy <= y2

                detected_objects = [obj for obj in detected_objects if inside_roi(obj)]

            nearest = None
            
            if detected_objects:
                candidate = max(detected_objects, key=lambda x: x[0])
                self.history.append(candidate)
                
                colors = [obj[2] for obj in self.history]
                dominant_color = max(set(colors), key=colors.count)
                
                candidates_color = [obj for obj in detected_objects if obj[2] == dominant_color]
                
                if candidates_color:
                    nearest = max(candidates_color, key=lambda x: x[0])
            
            self.obstacle = nearest
            
            for area, (x, y, w, h), color_name, color_bgr in detected_objects:
                label = f"{color_name} Colour"
                if nearest and (area == nearest[0] and color_name == nearest[2]):
                    label += " (nearest)"
                    cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 255), 3)
                else:
                    cv2.rectangle(imageFrame, (x, y), (x + w, y + h), color_bgr, 2)
                cv2.putText(imageFrame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_bgr, 2)
            cv2.putText(imageFrame, f"FPS: {self.fps:.1f}", (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
            if self.roi:
                (x1, y1), (x2, y2) = self.roi
                cv2.rectangle(imageFrame, (x1, y1), (x2, y2), (255, 255, 0), 2)
            with lock:
                self.display_frame = imageFrame
            time.sleep(0.03)
                
    def get_display_frame(self):
        with lock:
            return self.display_frame
    def terminate(self):
        self.end_thread = True
        self.thread.join()
        
    def get_nearest_box(self):
        with lock:
            return self.obstacle