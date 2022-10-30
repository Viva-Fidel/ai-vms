import sqlite3

from PySide6 import QtCore
from PySide6.QtWidgets import QLabel, QScrollArea, QSizePolicy
from PySide6.QtGui import QPixmap, QImage, QPalette

from camera import Camera


class Newcam:

    def __init__(self, camera_url, counter, row, column):
        self.camera_url = camera_url
        self.counter = counter
        self.row = row
        self.column = column

    def add_camera(self):
        con = sqlite3.connect('db\\user.db')
        cur = con.cursor()

        self.camera = QLabel()
        self.camera.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera.setScaledContents(True)
        self.camera.setObjectName(f"Camera_{self.counter}")

        cur.execute(f'SELECT DISTINCT Camera_name FROM camera_information')
        value = cur.fetchall()

        a = f"Camera_{self.counter}"

        if tuple([a]) not in value:
            cur.execute(
                f"INSERT INTO camera_information (Camera_URL, Camera_name, Camera_state, Camera_row, Camera_column) VALUES ('{self.camera_url}', 'Camera_{self.counter}', 'Normal', {self.row}, {self.column})")
            con.commit()

        self.QScrollArea = QScrollArea()
        self.QScrollArea.setBackgroundRole(QPalette.Dark)
        self.QScrollArea.setWidgetResizable(True)
        self.QScrollArea.setWidget(self.camera)

        self.CaptureIpCameraFramesWorker = Camera(self.camera_url)
        self.CaptureIpCameraFramesWorker.ImageUpdated.connect(lambda image: self.ShowCamera(image))

        self.CaptureIpCameraFramesWorker.start()

        cur.close()
        con.close()
        return self.QScrollArea

    @QtCore.Slot()
    def ShowCamera(self, frame: QImage) -> None:
        self.camera.setPixmap(QPixmap.fromImage(frame))
