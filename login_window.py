# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent
from gestor import users_gestor, wares_gestor
from main_window import Ui_MainWindow
from decouple import Config, RepositoryEnv

# DOTENV_FILE = 'C:/Users/IROJAS/Desktop/Genesis/genesis-system-admin/.env'
env_config = Config(RepositoryEnv('C:/Users/IROJAS/Desktop/Genesis/genesis-system-admin/.env'))


class Ui_LoginWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None): #para que puse el parent = None?
        super(Ui_LoginWindow, self).__init__(parent)
        #se crea el gestor de almacenes
        self.user_gest = users_gestor()     
        self.ware_gest = wares_gestor()

    def openMainWindow(self):
        # param1 es bool para existencia de usuario, param2 para ver usuario habilitado bool
        currentUser = self.user_gest.check_login(self.txtUser.text(),self.txtPwd.text())
        validator, objWares, currentWareName = self.ware_gest.exist_ware()
        # objWares = (curretWare: ware, restWares: list[ware])

        if bool(currentUser) and validator:
            # QMessageBox.information(self, 'Mensaje', "Log In Correcto", QMessageBox.Ok, QMessageBox.Ok)
            self.ui = Ui_MainWindow(currentUser, objWares[0], objWares[1], currentWareName)
            LoginWindow.close()
            self.ui.show()

        elif not(bool(currentUser)) and validator:
            self.label_message.setVisible(True)
        #puede ser falla de datos de de usuario en mysql
        #puede ser falla de que usuario o contraseña no coincidan

        elif not(validator) and bool(currentUser):
            QMessageBox.about(self, "Alerta", "Revisar datos de almacen")
        #puede ser falla de datos de wares en mysql
        #puede ser falla en datos de registro.txt

        elif not(validator) and not(bool(currentUser)):
            QMessageBox.about(self, "Alerta", "Revisar datos de almacen y usuario")


    # -----------  evento que se activa cuando se presiona enter  -----------
    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and
            (source is self.txtPwd or source is self.txtUser)):
            
            if event.text() == "\r":
                self.openMainWindow()
            #print('key press:', (event.key(), event.text()))
        return super(Ui_LoginWindow, self).eventFilter(source, event)

    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(380, 312)
        LoginWindow.setFixedSize(380,312)
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")

        # -----------  Login Button  -----------
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(True)
        self.pushButton.setGeometry(QtCore.QRect(70, 240, 230, 40))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(11)

        self.pushButton.setFont(font)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("background-color: rgb(189, 189, 189);\n"
"")
        self.pushButton.setIconSize(QtCore.QSize(300, 50))
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setAutoExclusive(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openMainWindow)
        # ======  End of Login Button  =======
        
        # -----------  text field for User  -----------
        self.txtUser = QtWidgets.QLineEdit(self.centralwidget)
        self.txtUser.setGeometry(QtCore.QRect(70, 110, 230, 40))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(11)
        self.txtUser.setFont(font)
        self.txtUser.setMaxLength(8)
        self.txtUser.setFrame(True)
        self.txtUser.setClearButtonEnabled(True)
        self.txtUser.setObjectName("txtUser")
        self.txtUser.installEventFilter(self) # metodo para llamar a funcion keypressed
        # ======  End of lineEdit_1  =======
        
        # -----------  text field for password  -----------
        
        self.txtPwd = QtWidgets.QLineEdit(self.centralwidget)
        self.txtPwd.setGeometry(QtCore.QRect(70, 170, 230, 40))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(11)
        self.txtPwd.setFont(font)
        self.txtPwd.setMaxLength(8)
        self.txtPwd.setFrame(True)
        self.txtPwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtPwd.setClearButtonEnabled(True)
        self.txtPwd.setObjectName("txtPwd")
        self.txtPwd.installEventFilter(self) #metodo para llamar a funcion keypressed
        # ======  End of password text field  =======
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(55, 30, 270, 54))
        self.label.setStyleSheet("")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(env_config.get('ROOT') + "imgs/login_user.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # -----------  wrongLogin label  -----------
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)

        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(65)

        self.label_message = QtWidgets.QLabel(self.centralwidget)
        self.label_message.setPalette(palette)
        self.label_message.setGeometry(QtCore.QRect(70, 195, 250, 54))
        self.label_message.setFont(font)
        self.label_message.setStyleSheet("")
        self.label_message.setText("Usuario o contraseña incorrecta")
        self.label_message.setObjectName("label_message")
        self.label_message.setVisible(False)

        # ======  End of wrongLogin label   =======
        LoginWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(LoginWindow)
        self.statusbar.setObjectName("statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Genesis - [Museo del Libro]"))
        self.pushButton.setText(_translate("LoginWindow", "Log in"))
        self.txtUser.setPlaceholderText(_translate("LoginWindow", "User"))
        self.txtPwd.setPlaceholderText(_translate("LoginWindow", "Password"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    app.exec_()
    enable_datetime = False

