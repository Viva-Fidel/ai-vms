import cv2


class Person_detection_basic:
    def __init__(self, frame):
        self.frame = frame
        self.fullbody_cascade = cv2.CascadeClassifier('basic_analytics/haarcascade_fullbody.xml')

    def detect_person(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self.fullbody_cascade.detectMultiScale(gray, 1.03, 3)
        for (x, y, w, h) in faces:
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 250, 0), 2)
