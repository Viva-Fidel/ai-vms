import cv2
import time

from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QImage

from face_detection_basic import Face_detection_basic
from face_detection_advanced import Face_detection_advanced
from person_detection_basic import Person_detection_basic
from person_detection_advanced import Person_detection_advanced
from threading import Thread


class Camera(QThread):
    ImageUpdated = Signal(QImage)

    all = []
    i = -1

    def __init__(self, url) -> None:
        super(Camera, self).__init__()
        self.url = url
        self.__thread_active = True
        self.fps = 0
        self.__thread_pause = False
        self.face_detection_basic = False
        self.face_detection_advanced = False
        self.person_detection_basic = False
        self.person_detection_advanced = False
        Camera.all.append(self)

    def start(self):
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
        return self

    def run(self) -> None:

        cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        while cap.isOpened():
            FPS = 0.01
            ret, frame = cap.read()
            time.sleep(FPS)

            if self.face_detection_basic:
                fd = Face_detection_basic(frame)
                fd.detect_face()

            if self.face_detection_advanced:
                fd = Face_detection_advanced(frame)
                fd.detect_face()

            if self.person_detection_basic:
                pd = Person_detection_basic(frame)
                pd.detect_person()

            if self.person_detection_advanced:
                pd = Person_detection_advanced(frame)
                pd.detect_person()

            height, width, channels = frame.shape

            bytes_per_line = width * channels

            if ret:

                cv_rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                qt_rgb_image = QImage(cv_rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)

                qt_rgb_image_scaled = qt_rgb_image.scaled(1280, 720, Qt.KeepAspectRatio)

                self.ImageUpdated.emit(qt_rgb_image_scaled)

            else:
                break

        cap.release()

    def switch_off(self):
        Camera.all[Camera.i].face_detection_basic = False
        Camera.all[Camera.i].face_detection_advanced = False
        Camera.all[Camera.i].person_detection_basic = False
        Camera.all[Camera.i].person_detection_advanced = False

    def face_detection_basic_on(self):
        Camera.all[Camera.i].face_detection_basic = True

    def face_detection_advanced_on(self):
        Camera.all[Camera.i].face_detection_advanced = True

    def person_detection_basic_on(self):
        Camera.all[Camera.i].person_detection_basic = True

    def person_detection_advanced_on(self):
        Camera.all[Camera.i].person_detection_advanced = True
