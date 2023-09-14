from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from ware_dialog import Ui_Dialog
from datetime import datetime # estos es para mostrar la hora en el main
# import threading
import time
from datetime import datetime
from decouple import Config, RepositoryEnv
from objects import user, ware

enable_datetime = True
env_config = Config(RepositoryEnv('C:/Users/IROJAS/Desktop/Genesis/genesis-system-admin/.env'))

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, currentUser: user = None, currentWare: ware = None, restWare: list = None, wareName:str = None, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        # currentWare: ware , datos de almacen actual
        # restWare: list[ware], datos de los demas almacenes
        # currentUser: user, datos de usuario actual
        self.ware_name = wareName
        self.usr_text = currentUser.user

        #NOS QUEDAMOS EN ESTA PARTE
        # self.dialog = QDialog()
        # self.ui_dialog = Ui_Dialog(data_user, data_ware, self.dialog)
        self.setupUi()

    # -----------  close event configuration  -----------
    def closeEvent(self, event):
        # self.accept()
        event.accept()
        self.destroy()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1280, 1024)
        self.setFixedSize(1280, 1024)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")


        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1280, 100))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(83, 97, 142, 255), stop:1 rgba(97, 69, 128, 255));")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.userName = QtWidgets.QLabel(self.frame)
        self.userName.setGeometry(QtCore.QRect(1060, 20, 191, 31))

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)

        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.userName.setPalette(palette)
        self.userName.setFont(font)
        self.userName.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.userName.setObjectName("userName")

        self.wareName = QtWidgets.QLabel(self.frame)
        self.wareName.setGeometry(QtCore.QRect(780, 60, 255, 31))
        self.wareName.setPalette(palette)
        self.wareName.setFont(font)
        self.wareName.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.wareName.setObjectName("wareName")

        self.date_label = QtWidgets.QLabel(self.frame)
        self.date_label.setGeometry(QtCore.QRect(1060, 60, 191, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.date_label.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.date_label.setFont(font)
        self.date_label.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.date_label.setObjectName("date_label")
        # -----------  warelabel cofiguration  -----------

        self.wareIcon = QtWidgets.QLabel(self.frame)
        self.wareIcon.setGeometry(QtCore.QRect(30, 15, 72, 72))
        self.wareIcon.setText("")
        self.wareIcon.setPixmap(QtGui.QPixmap(env_config.get('ROOT') + "imgs/warehouse_icon.png"))
        self.wareIcon.setScaledContents(True)
        self.wareIcon.setObjectName("wareIcon")
        self.wareIcon.mousePressEvent = self.open_wareWindow


        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 737, 1280, 287))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(env_config.get('ROOT') + "imgs/main_window_button.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.notification_table = QtWidgets.QTableWidget(self.centralwidget)
        self.notification_table.setEnabled(False)
        self.notification_table.setGeometry(QtCore.QRect(0, 120, 1280, 617))
        self.notification_table.setObjectName("notification_table")
        self.notification_table.setColumnCount(3)
        self.notification_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.notification_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.notification_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.notification_table.setHorizontalHeaderItem(2, item)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 100, 1280, 20))
        self.frame_2.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        #QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # QtCore.QMetaObject.connectSlotsByName(self)
        # self.run_threads()

    def open_wareWindow(self, event):
        self.ui_dialog.init_condition()
        self.setEnabled(False)
        self.ui_dialog.show_window()
        if self.ui_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.setEnabled(True)

    def update_datetime(self):
        while(enable_datetime):
            self.date_label.setText(datetime.now().strftime("%H:%M %d/%m/%Y"))
            time.sleep(0.5)

    # def run_threads(self):
    #     self.t1 = threading.Thread(target=self.update_datetime)
    #     self.t1.start()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Genesis - [Museo del Libro]"))
        self.userName.setText(_translate("MainWindow", "USER: " + self.usr_text.upper()))
        self.date_label.setText(_translate("MainWindow", "18:39 20/04/2021"))
        self.wareName.setText(_translate("MainWindow", "ALMACEN: " + self.ware_name.upper()))
        self.wareName.adjustSize() #Ajusta el tamaño del label al tamaño de las letras
        self.wareName.move(1040 - self.wareName.width(),66) #cambia la posicion del label

        item = self.notification_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "N°"))
        item = self.notification_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Notificación"))
        item = self.notification_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Estado"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    sys.exit(app.exec_())