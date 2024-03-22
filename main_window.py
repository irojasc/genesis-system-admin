from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from ware_dialog import Ui_Dialog
from datetime import datetime # estos es para mostrar la hora en el main
# from gestor import users_gestor
from decouple import Config, RepositoryEnv
from objects import user, ware
from datetime import datetime
from uiConfigurations import *
import time
import threading

env_config = Config(RepositoryEnv('C:/Users/IROJAS/Desktop/Genesis/genesis-system-admin/.env'))

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, currentUser: user = None, currentWare: ware = None, restWare: list = None, wareName:str = None, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.enable_datetime = True
        self.WareProdDate = datetime.now().date()
        self.notification_list = []
        # currentWare: ware , datos de almacen actual
        # restWare: list[ware], datos de los demas almacenes
        # currentUser: user, datos de usuario actual
        self.currentUser = currentUser
        self.ware_name = wareName
        self.usr_text = currentUser.user
        #NOS QUEDAMOS EN ESTA PARTE
        self.dialog = QDialog()
        self.uiWareProduct = Ui_Dialog(currentUser, currentWare, restWare, self.WareProdDate, self.dialog)
        self.setupUi()

    def openWareDialog(self, event):
        if self.currentUser.auth["productSrch"]:
            self.uiWareProduct.init_condition()
            self.setEnabled(False)
            self.uiWareProduct.showWindow()
            if self.uiWareProduct.exec_() == QtWidgets.QDialog.Accepted:
                self.setEnabled(True)
        else:
            QMessageBox.about(self, "Alerta", "No tiene permisos para ingresar almacen")
    
    def loadNotificationTable(self):
        
        
        
        #flag = QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled
        self.notification_table.setRowCount(len(self.notification_list))
        
        for row, ware_li in enumerate(self.notification_list):
            item = QtWidgets.QTableWidgetItem(ware_li["cod"])
            #item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            self.notification_table.setItem(row, 0, item)

            item = QtWidgets.QTableWidgetItem(ware_li["operacion"])
            #item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            self.notification_table.setItem(row, 1, item)
            txt = "[" + ware_li["s_point"] + "]-->[" + ware_li["f_point"] + "]"
            self.notification_table.item(row, 1).setToolTip(txt)

            item = QtWidgets.QTableWidgetItem(str.upper(ware_li["receiver"]))
            #item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            self.notification_table.setItem(row, 2, item)
            txt = "I:" + str.upper(ware_li["emiter"]) + "\nD:" + str.upper(ware_li["receiver"])
            self.notification_table.item(row, 2).setToolTip(txt)

            item = QtWidgets.QTableWidgetItem(ware_li["detalles"].replace('\n', ""))
            #item.setFlags(flag)
            self.notification_table.setItem(row, 3, item)
            self.notification_table.item(row, 3).setToolTip(ware_li["detalles"])

            item = QtWidgets.QTableWidgetItem(str(ware_li["f_date"]))
            #item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            self.notification_table.setItem(row, 4, item)
            txt = "I:" + ware_li["s_date"] + "\nD:" + ware_li["f_date"]
            self.notification_table.item(row, 4).setToolTip(txt)

            item = QtWidgets.QTableWidgetItem(ware_li["estado"])
            #item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            self.notification_table.setItem(row, 5, item)
            if ware_li["estado"] == "ATENDIDO":
                self.notification_table.item(row, 5).setBackground(
                    QtGui.QColor(ware_li["colors"]["amarillo"][0], ware_li["colors"]["amarillo"][1],
                                 ware_li["colors"]["amarillo"][2]))

            elif ware_li["estado"] == "CERRADO":
                self.notification_table.item(row, 5).setBackground(
                    QtGui.QColor(ware_li["colors"]["verde"][0], ware_li["colors"]["verde"][1],
                                 ware_li["colors"]["verde"][2]))

            elif ware_li["estado"] == "OBSERVADO":
                self.notification_table.item(row, 5).setBackground(
                    QtGui.QColor(ware_li["colors"]["rojo"][0], ware_li["colors"]["rojo"][1],
                                 ware_li["colors"]["rojo"][2]))
    
    
    
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1280, 700)
        self.setFixedSize(1280, 700)
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

        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.userName.setPalette(getUserNamePalette())
        self.userName.setFont(font)
        self.userName.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.userName.setObjectName("userName")

        self.wareName = QtWidgets.QLabel(self.frame)
        self.wareName.setGeometry(QtCore.QRect(780, 60, 255, 31))
        self.wareName.setPalette(getUserNamePalette())
        self.wareName.setFont(font)
        self.wareName.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.wareName.setObjectName("wareName")

        self.dateText = QtWidgets.QLabel(self.frame)
        self.dateText.setGeometry(QtCore.QRect(1060, 60, 191, 31))
        self.dateText.setPalette(getDatePalette())
        self.dateText.setFont(font)
        self.dateText.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.dateText.setObjectName("dateText")
        # -----------  warelabel cofiguration  -----------

        self.wareIcon = QtWidgets.QLabel(self.frame)
        self.wareIcon.setGeometry(QtCore.QRect(30, 15, 72, 72))
        self.wareIcon.setText("")
        self.wareIcon.setPixmap(QtGui.QPixmap(env_config.get('ROOT') + "imgs/warehouse_icon.png"))
        self.wareIcon.setScaledContents(True)
        self.wareIcon.setObjectName("wareIcon")
        self.wareIcon.mousePressEvent = self.openWareDialog

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
        self.notification_table.setColumnCount(6)

        # self.notification_table.setRowCount(0)

        
        self.notification_table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Código'))
        self.notification_table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Operación'))
        self.notification_table.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('Responsable'))
        self.notification_table.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem('Detalles'))
        self.notification_table.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem('Fecha'))
        self.notification_table.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem('Estado'))
        self.notification_table.setColumnWidth(0, 80)
        self.notification_table.setColumnWidth(1, 120)
        self.notification_table.setColumnWidth(2, 120)
        self.notification_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.notification_table.setColumnWidth(4, 120)
        self.notification_table.setColumnWidth(5, 120)

        self.notification_table.horizontalHeader().setEnabled(False)
        self.notification_table.setSelectionBehavior(1)
        self.notification_table.setSelectionMode(1)
        self.notification_table.verticalHeader().hide()
        # self.notification_table.itemDoubleClicked.connect(self.doubleClickItem)
        
        # ------------------  frame_2 configuration
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 100, 1280, 20))
        self.frame_2.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        #QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.run_threads()

    def closeEvent(self, event):
        self.enable_datetime = False
        event.accept()

    def update_datetime(self):
        while(self.enable_datetime):
            self.dateText.setText(datetime.now().strftime("%H:%M %d/%m/%Y"))
            time.sleep(0.5)

    def run_threads(self):
        self.t1 = threading.Thread(target=self.update_datetime)
        self.t1.start()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Genesis - [Museo del Libro]"))
        self.userName.setText(_translate("MainWindow", "USER: " + self.usr_text.upper()))
        self.dateText.setText(_translate("MainWindow", "18:39 20/04/2021"))
        self.wareName.setText(_translate("MainWindow", "ALMACEN: " + self.ware_name.upper()))
        self.wareName.adjustSize() #Ajusta el tamaño del label al tamaño de las letras
        self.wareName.move(1040 - self.wareName.width(),66) #cambia la posicion del label

        font = QtGui.QFont("Open Sans Semibold",10, 85)
        font.setBold(True)

        self.notification_table.horizontalHeaderItem(0).setFont(font)
        self.notification_table.horizontalHeaderItem(0).setForeground(QBrush(QColor(0, 0, 0)))
        self.notification_table.horizontalHeaderItem(1).setFont(font)
        self.notification_table.horizontalHeaderItem(1).setForeground(QBrush(QColor(0, 0, 0)))
        self.notification_table.horizontalHeaderItem(2).setFont(font)
        self.notification_table.horizontalHeaderItem(2).setForeground(QBrush(QColor(0, 0, 0)))
        self.notification_table.horizontalHeaderItem(3).setFont(font)
        self.notification_table.horizontalHeaderItem(3).setForeground(QBrush(QColor(0, 0, 0)))
        self.notification_table.horizontalHeaderItem(4).setFont(font)
        self.notification_table.horizontalHeaderItem(4).setForeground(QBrush(QColor(0, 0, 0)))
        self.notification_table.horizontalHeaderItem(5).setFont(font)
        self.notification_table.horizontalHeaderItem(5).setForeground(QBrush(QColor(0, 0, 0)))
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    sys.exit(app.exec_())