import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


class Face_detection_advanced:
    def __init__(self, frame):
        self.frame = frame

    def detect_face(self):
        with mp_face_detection.FaceDetection(
                model_selection=0, min_detection_confidence=0.2) as face_detection:
            self.frame.flags.writeable = False
            results = face_detection.process(self.frame)
            self.frame.flags.writeable = True
            if results.detections:
                for detection in results.detections:
                    detection = str(detection).split()
                    print(detection)
                    x = round(float(detection[detection.index('xmin:') + 1]) * 650)
                    y = round(float(detection[detection.index('ymin:') + 1]) * 450)
                    w = round(float(detection[detection.index('width:') + 1]) * 600)
                    h = round(float(detection[detection.index('height:') + 1]) * 600)
                    faces = [[x, y, w, h]]
                    for (x, y, w, h) in faces:
                        cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 250, 0), 2)
