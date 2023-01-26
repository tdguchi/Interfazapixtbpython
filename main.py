#!/usr/bin/env python3
from PyQt5 import QtCore, QtGui, QtWidgets
from XTBApi.api import Client
import time
import concurrent.futures

class Ui_MainWindow(object):
    f = open("Python.txt", "r")
    i = int(f.read())

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(310, 360)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Largo = QtWidgets.QPushButton(self.centralwidget)
        self.Largo.setGeometry(QtCore.QRect(100, 20, 121, 41))
        self.Largo.setAutoFillBackground(False)
        self.Largo.setText("")
        self.Largo.clicked.connect(self.showMessageLargo)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "/home/pablo/aplicacion/green_up_arrow_preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Largo.setIcon(icon)
        self.Largo.setIconSize(QtCore.QSize(32, 32))
        self.Largo.setObjectName("Largo")
        self.Modificar = QtWidgets.QPushButton(self.centralwidget)
        self.Modificar.setGeometry(QtCore.QRect(0, 20, 121, 41))
        self.Modificar.setAutoFillBackground(False)
        self.Modificar.setText("")
        self.Modificar.clicked.connect(self.showMessageModificar)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "/home/pablo/aplicacion/green_up_arrow_preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Modificar.setIcon(icon)
        self.Modificar.setIconSize(QtCore.QSize(32, 32))
        self.Modificar.setObjectName("Modificar")
        self.Corto = QtWidgets.QPushButton(self.centralwidget)
        self.Corto.setGeometry(QtCore.QRect(100, 90, 121, 41))
        self.Corto.setText("")
        self.Corto.clicked.connect(self.showMessageCorto)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(
            "/home/pablo/aplicacion/arrow-157087_960_720.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Corto.setIcon(icon1)
        self.Corto.setIconSize(QtCore.QSize(32, 32))
        self.Corto.setObjectName("Corto")
        self.CerrarTodo = QtWidgets.QPushButton(self.centralwidget)
        self.CerrarTodo.setGeometry(QtCore.QRect(80, 290, 150, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.CerrarTodo.setFont(font)
        self.CerrarTodo.setObjectName("CerrarTodo")
        self.CerrarTodo.clicked.connect(self.closeall)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(60, 220, 71, 41))
        self.comboBox.setObjectName("comboBox")
        self.Cerrar = QtWidgets.QPushButton(self.centralwidget)
        self.Cerrar.setGeometry(QtCore.QRect(150, 220, 111, 41))
        self.Cerrar.setObjectName("Cerrar")
        self.Cerrar.clicked.connect(self.close)
        self.Actualizar = QtWidgets.QPushButton(self.centralwidget)
        self.Actualizar.setGeometry(QtCore.QRect(50, 170, 231, 25))
        self.Actualizar.setObjectName("Actualizar")
        self.Actualizar.clicked.connect(self.actualizarlista)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "A invertir"))
        self.CerrarTodo.setText(_translate("MainWindow", "Cerrar todo"))
        self.Cerrar.setText(_translate("MainWindow", "Cerrar"))
        self.Actualizar.setText(_translate(
            "MainWindow", "Actualizar lista de operaciones"))

    argumentos = []
        
    def showMessageLargo(self):
        result = QtWidgets.QMessageBox.question(self.Largo, 'Título', 'Vas a entrar largo en el Nasdaq, ¿estás seguro?',
                                                QtWidgets.QMessageBox.Yes | 
        QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            self.sistema("buy", self.i)

    def showMessageCorto(self):
        result = QtWidgets.QMessageBox.question(self.Corto, 'Título', 'Vas a entrar corto en el Nasdaq, ¿estás seguro?',
                                                QtWidgets.QMessageBox.Yes | 
        QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            self.sistema("sell", self.i)
    
    def showMessageModificar(self):
        result = QtWidgets.QMessageBox.question(self.Modificar, 'Título', 'Vas a modificar la orden, ¿estás seguro?',
                                                QtWidgets.QMessageBox.Yes | 
        QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            self.sistema("Buy", self.i, 9800)

    def operar(self, tipo, comentario, sl, usuario, password):
        client = Client()
        client.login(usuario, password, mode="demo")
        client.check_if_market_open(["US100"])
        client.open_trade(tipo, "US100", 0.02, str(comentario))
        time.sleep(3)
        client.logout()

    def closeselected(self, usuario, password):
        client = Client()
        client.login(usuario, password, mode="demo")
        id_seleccionado = self.comboBox.currentData()
        for trade in client.get_trades():
            if trade["comment"] == id_seleccionado:
                client.close_trade(trade["order"])
                time.sleep(0.2)
        time.sleep(3)
        client.logout()

    def closeallselected(self, usuario, password):
        client = Client()
        client.login(usuario, password, mode="demo")
        client.close_all_trades()
        time.sleep(3)
        client.logout()

    def closeall(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            resultados = [executor.submit(
                self.closeallselected, *args) for args in self.argumentos]
        self.actualizarlista()

    def close(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            resultados = [executor.submit(self.closeselected, *args) for args in self.argumentos]
        self.actualizarlista()

    def sistema(self, tipo, comentario, sl):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            resultados = [executor.submit(
                self.operar, tipo, comentario, sl, *args) for args in self.argumentos]
        self.i = self.i + 1
        file = open("Python.txt", "w")
        file.write(str(self.i))
        file.close()
        self.actualizarlista()

    def actualizarlista(self):
        self.comboBox.clear()
        client = Client()
        client.login("14162943", "Terapiatdg@@26", mode="demo")
        trades = client.get_trades()
        for trade in trades:
            self.comboBox.addItem(str(trade["comment"]), trade["comment"])
        time.sleep(3)
        client.logout()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
