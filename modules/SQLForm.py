# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout

class SQLForm(QWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.te = QTextEdit()
        self.pb = QPushButton('Выполнить')
        self.lay = QVBoxLayout()
        self.lay.addWidget(self.te)
        self.lay.addWidget(self.pb)
        self.setLayout(self.lay)
        self.setWindowTitle("Выполнение запроса")
        self.parentForm = parent
        self.pb.clicked.connect(self.Click)

    def Click(self):
        self.close()


