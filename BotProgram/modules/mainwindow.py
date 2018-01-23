## -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import uic
from DataBaseForm import  DataBaseForm

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/mainwindow.ui", self)
        self.labToolBar = QLabel('<font color=red>Бот не запущен в Telegram<font>')
        self.statusBar.addWidget(self.labToolBar)
        self.DB.triggered.connect(self.openDataBaseForm)

    def openDataBaseForm(self):
        self.f = DataBaseForm()
        self.f.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())