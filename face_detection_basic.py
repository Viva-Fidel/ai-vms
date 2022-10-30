import cv2


class Face_detection_basic:
    def __init__(self, frame):
        self.frame = frame
        self.face_cascade = cv2.cuda_CascadeClassifier('basic_analytics/haarcascade_frontalface_default.xml')

    def detect_face(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                                   minNeighbors=8,
                                                   minSize=(30, 30),
                                                   flags=cv2.CASCADE_SCALE_IMAGE)
        for (x, y, w, h) in faces:
            print(x, y, w, h)
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 250, 0), 2)
