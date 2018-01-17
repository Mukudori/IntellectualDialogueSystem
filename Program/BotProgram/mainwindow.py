## -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import DataBase
from DataBaseForm import  DataBaseForm

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("mainwindow.ui", self)
        #data = DataBase.GetTable("SELECT * FROM wordsgrouptab")
        #self.lineEdit.setText(str(data[6]['semantic']))
        self.DB.triggered.connect(self.openDataBaseForm)

    def openDataBaseForm(self):
        self.f = DataBaseForm()
        self.f.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())