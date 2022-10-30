import sys
import sqlite3

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QInputDialog
from PySide6.QtGui import QAction
from PySide6.QtCore import Slot, QEvent, QSettings, Qt

from analyticsmenu import Analytics_menu
from newcam import Newcam


class VMS(QMainWindow):
    counter = 0
    grid_counter = [[0, 0], [0, 1], [1, 0], [1, 1]]

    def __init__(self):
        super(VMS, self).__init__()

        self.SetupUI()

    def SetupUI(self):

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.widget = QWidget(self)
        self.widget.setLayout(self.grid_layout)

        self.setCentralWidget(self.widget)
        self.setStyleSheet("QMainWindow {background: 'black';}")

        self.setWindowTitle("aiVMS")

        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuCameras = QtWidgets.QMenu(self.menuMenu)
        self.menuCameras.setObjectName("menuCameras")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.actionAdd_camera = QAction()
        self.actionAdd_camera.setObjectName("actionAdd_camera")
        self.menuCameras.addAction(self.actionAdd_camera)

        self.actionDelete_camera = QAction()
        self.actionDelete_camera.setObjectName("actionDelete_camera")
        self.menuCameras.addAction(self.actionDelete_camera)

        self.menuMenu.addAction(self.menuCameras.menuAction())
        self.menubar.addAction(self.menuMenu.menuAction())

        try:
            self.load_camera()
        except:
            pass

        self.actionAdd_camera.setCheckable(False)
        self.actionAdd_camera.triggered.connect(lambda: self.add_camera())

        self.actionDelete_camera.setCheckable(False)
        self.actionDelete_camera.triggered.connect(lambda: self.delete_camera())

        # Loading last window size and position
        self.settings = QSettings("CVLab", "aiVMS")

        try:
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))
        except:
            pass

        self.retranslateUi()

    @Slot()
    def add_camera(self):
        if VMS.counter == 4:
            return None
        else:
            camera_url, _ = QInputDialog.getText(self, 'Adding new camera',
                                                 'Enter RSTP link:')
            row, column = VMS.grid_counter[VMS.counter]
            nc = Newcam(camera_url, VMS.counter, row, column)
            self.grid_layout.addWidget(nc.add_camera(), row, column)
            VMS.counter += 1
            nc.QScrollArea.installEventFilter(self)
            self.setCentralWidget(self.widget)

    def delete_camera(self):
        if VMS.counter == 0:
            return None
        else:
            con = sqlite3.connect('C:\\Users\\a.artamonov\\PycharmProjects\\aiVMS\\db\\user.db')
            cur = con.cursor()
            cur.execute(f'SELECT* FROM camera_information ORDER BY Camera_ID DESC LIMIT 1')
            value = cur.fetchall()
            cur.execute(f'DELETE FROM camera_information WHERE Camera_ID IN {value[0]}')
            VMS.counter -= 1
            row, column = VMS.grid_counter[VMS.counter]
            con.commit()
            cur.close()

            self.grid_layout.itemAtPosition(row, column).widget().setParent(None)

    @Slot()
    def load_camera(self):
        con = sqlite3.connect('db\\user.db')
        cur = con.cursor()

        cur.execute(f'SELECT* FROM camera_information')
        value = cur.fetchall()

        for i in range(len(value)):
            nc = Newcam(value[i][2], VMS.counter, value[i][4], value[i][5])
            self.grid_layout.addWidget(nc.add_camera(), value[i][4], value[i][5])

            VMS.counter += 1
            nc.QScrollArea.installEventFilter(self)
            self.setCentralWidget(self.widget)

        cur.close()
        con.close()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            con = sqlite3.connect('db\\user.db')
            cur = con.cursor()
            cur.execute(f'SELECT* FROM camera_information')
            value = cur.fetchall()
            for i in range(len(value)):
                if source == self.grid_layout.itemAtPosition(value[i][4], value[i][5]).widget() and value[i][
                    3] == "Normal":
                    cur.execute(
                        f"UPDATE camera_information SET Camera_state = 'Maximized' WHERE Camera_name = '{value[i][1]}'")
                    con.commit()
                    cur.close()

                    cur = con.cursor()
                    cur.execute(f'SELECT* FROM camera_information')
                    value = cur.fetchall()

                    for k in range(len(value)):
                        print(value)
                        if value[k][3] == "Normal":
                            self.grid_layout.itemAtPosition(value[k][4], value[k][5]).widget().hide()

                    cur.close()
                    con.close()
                    return True
                if source == self.grid_layout.itemAtPosition(value[i][4], value[i][5]).widget() and value[i][
                    3] == "Maximized":
                    cur.execute(
                        f"UPDATE camera_information SET Camera_state = 'Normal' WHERE Camera_name = '{value[i][1]}'")
                    con.commit()
                    for k in range(len(value)):
                        print(value)
                        if value[k][3] == "Normal":
                            self.grid_layout.itemAtPosition(value[k][4], value[k][5]).widget().show()

                    cur.close()
                    con.close()
                    return True

        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.RightButton:
                con = sqlite3.connect('db\\user.db')
                cur = con.cursor()
                cur.execute(f'SELECT* FROM camera_information')
                value = cur.fetchall()
                for i in range(len(value)):
                    if source == self.grid_layout.itemAtPosition(value[i][4], value[i][5]).widget():
                        self.contextMenuEvent(event, i)
                return True

        else:
            return super().eventFilter(source, event)

    def contextMenuEvent(self, *args):

        self.contextMenu = QtWidgets.QMenu(self)

        self.actionAnalytics_Menu = QAction()
        self.actionAnalytics_Menu = self.contextMenu.addAction("Open analytics menu")

        self.action = self.contextMenu.exec(args[0].globalPos())

        self.actionAnalytics_Menu.triggered.connect(self.choose_analytics(args[1]))

    def choose_analytics(self, i):
        self.window = QtWidgets.QMainWindow()
        self.ui = Analytics_menu(i)
        self.ui.setupUi(self.window)
        self.window.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        (_translate("VMS", "MainWindow"))
        self.menuMenu.setTitle(_translate("VMS", "Menu"))
        self.menuCameras.setTitle(_translate("VMS", "Cameras"))
        self.actionAdd_camera.setText(_translate("VMS", "Add camera"))
        self.actionDelete_camera.setText(_translate("VMS", "Delete camera"))

    def closeEvent(self, event) -> None:
        self.settings.setValue('window size', self.size())
        self.settings.setValue('window position', self.pos())

        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = VMS()
    widget.show()

    sys.exit(app.exec())
