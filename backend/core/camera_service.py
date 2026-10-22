import cv2
import time
import asyncio
from fastapi import WebSocket

class CameraService:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = None
        self.is_running = False

    def start(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.camera_id)
            self.is_running = True

    def stop(self):
        if self.cap:
            self.cap.release()
            self.cap = None
            self.is_running = False

    def get_frame(self):
        if self.is_running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def detect_faces(self, frame):
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))
        
        detections = []
        for (x, y, w, h) in faces:
            detections.append({
                "bbox": [int(x), int(y), int(w), int(h)],
                "score": 1.0
            })
        return detections