from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, \
    QPushButton, QComboBox
from clients_subsystem.rii.database.CathGroupModule import CathGroup
from clients_subsystem.rii.database.ClientModule import Client
from clients_subsystem.rii.database.CathedraModule import Cathedra

class OpenTimeTableForm(QWidget):
    def __init__(self):
        super().__init__()
        self.SelectedGroups = {'None': 0, 'Students' : 1, 'Teachers' : 2}
        self.initUI()


    def initUI(self):
        vLay = QVBoxLayout()
        hl1 = QHBoxLayout()
        self.lab1 = QLabel('Группа клиентов : ')
        self.cbClientsGroup = QComboBox()
        self.cbClientsGroup.addItems(['Студенты', 'Преподаватели'])
        hl1.addWidget(self.lab1)
        hl1.addWidget(self.cbClientsGroup)
        vLay.addLayout(hl1)

        hl2 = QHBoxLayout()
        self.lab2 = QLabel('Кафедра : ')
        self.cbCathedra = QComboBox()
        hl2.addWidget(self.lab2)
        hl2.addWidget(self.cbCathedra)
        self.cathList = Cathedra().getList()
        for row in self.cathList:
            self.cbCathedra.addItem(row['name'])
        vLay.addLayout(hl2)


        hl3 = QHBoxLayout()
        self.lab3 = QLabel('Группа студентов: ')
        self.cbGroup = QComboBox()
        hl3.addWidget(self.lab3)
        hl3.addWidget(self.cbGroup)
        vLay.addLayout(hl3)

        self.pbSave = QPushButton('Открыть')
        vLay.addWidget(self.pbSave)

        self.connectSlots()
        self.initStudent()

        self.setLayout(vLay)
        self.setWindowTitle('Открытие расписания занятий')

    def initStudent(self):
        self.selGroup = 1
        self.cbClientsGroupSelected = True
        self.lab3.setText('Группа : ')
        self.cbGroup.clear()
        self.stGroup = CathGroup().getList(idCath=self.getSelectedIDCath())
        for row in self.stGroup:
            self.cbGroup.addItem(row['name'])

    def getSelectedIDCath(self):
        idCath = self.cathList[self.cbCathedra.currentIndex()]['id']
        return idCath

    def initTeachers(self):
        self.selGroup = 2
        self.lab3.setText('ФИО : ')
        self.cbGroup.clear()

        self.teachList = Client().getTeachersListFromIDCath(
            idCath=self.getSelectedIDCath())
        self.cbGroup.addItems([row['shortfio'] for row in self.teachList])

    def initClient(self):
        if self.cbClientsGroup.currentText()=='Студенты':
            self.initStudent()
        else:
            self.initTeachers()

    def connectSlots(self):
        self.cbCathedra.currentIndexChanged.connect(self.initClient)
        self.cbClientsGroup.currentIndexChanged.connect(self.initClient)