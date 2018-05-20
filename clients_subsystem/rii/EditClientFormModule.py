

    def initUI(self):
        vLay = QVBoxLayout()

        h1 = QHBoxLayout()from clients_subsystem.rii.database.CathGroupModule import CathGroup
from clients_subsystem.rii.database.ClientModule import Client
from clients_subsystem.rii.database.CathedraModule import Cathedra
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QPushButton, QComboBox


class EditClientForm (QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.lab1 = QLabel('Группа клиентов')
        self.cbClientGroup = QComboBox()
        h1.addWidget(self.lab1)
        h1.addWidget(self.cbClientGroup)
        vLay.addLayout(h1)

        h2 = QHBoxLayout()
        self.lab2 = QLabel('Кафедра')
        self.cbCath = QComboBox()
        h2.addWidget(self.lab1)
        h2.addWidget(self.cbCath)
        vLay.addLayout(h2)

        h3 = QHBoxLayout()
        self.labClient = QLabel('ФИО/Група')
        self.cbClient = QComboBox()
        h3.addWidget(self.labClient)
        h3.addWidget(self.cbClient)
        vLay.addLayout(h3)

        h4 = QHBoxLayout()
        self.lab4 = QLabel('Telegram ID : ')
        self.leTelegram = QLineEdit()
        h4.addWidget(self.lab4)
        h4.addWidget(self.leTelegram)
        vLay.addLayout(h4)

        self.pb = QPushButton('Сохранить')
        vLay.addWidget(self.pb)

        self.setLayout(vLay)
        self.setWindowTitle('Редактирование информации о клиенте')

    def initClientsGroup(self):
        pass

    def initCath(self):
        pass

    def initStudents(self):
        pass

    def initTeachers(self):
        pass

    def connectSlots(self):
        pass

    def initEdit(self):
        pass

    def save(self):
        pass