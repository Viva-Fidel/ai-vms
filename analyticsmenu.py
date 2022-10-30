from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSettings
from PySide6.QtWidgets import QRadioButton

from camera import Camera


class Analytics_menu:
    def __init__(self, i):
        self.i = i

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Analytics Menu")
        Form.resize(300, 200)
        self.radioButton = QRadioButton(Form)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(20, 20, 180, 14))

        self.radioButton_2 = QRadioButton(Form)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(20, 40, 180, 14))
        self.radioButton_3 = QRadioButton(Form)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setGeometry(QRect(20, 60, 180, 14))
        self.radioButton_4 = QRadioButton(Form)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setGeometry(QRect(20, 80, 180, 14))
        self.radioButton_5 = QRadioButton(Form)
        self.radioButton_5.setObjectName(u"radioButton_5")
        self.radioButton_5.setGeometry(QRect(20, 100, 180, 14))

        self.settings = QSettings("CVLab", "Analytics Menu")

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
        self.radioButton.clicked.connect(lambda: self.switch_off())
        self.radioButton_2.clicked.connect(lambda: self.switch_on_basic_face_detection())
        self.radioButton_3.clicked.connect(lambda: self.switch_on_advanced_face_detection())
        self.radioButton_4.clicked.connect(lambda: self.switch_on_basic_person_detection())
        self.radioButton_5.clicked.connect(lambda: self.switch_on_advanced_person_detection())

    def switch_off(self):
        Camera.i = self.i
        Camera.switch_off(self)

    def switch_on_basic_face_detection(self):
        Camera.i = self.i
        Camera.face_detection_basic_on(self)

    def switch_on_advanced_face_detection(self):
        Camera.i = self.i
        Camera.face_detection_advanced_on(self)

    def switch_on_basic_person_detection(self):
        Camera.i = self.i
        Camera.person_detection_basic_on(self)

    def switch_on_advanced_person_detection(self):
        Camera.i = self.i
        Camera.person_detection_advanced_on(self)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.radioButton.setText(QCoreApplication.translate("Form", u"None", None))
        self.radioButton_2.setText(QCoreApplication.translate("Form", u"Face detection (Basic)", None))
        self.radioButton_3.setText(QCoreApplication.translate("Form", u"Face detection (Advanced)", None))
        self.radioButton_4.setText(QCoreApplication.translate("Form", u"Person detection (Basic)", None))
        self.radioButton_5.setText(QCoreApplication.translate("Form", u"Person detection (Advanced)", None))
