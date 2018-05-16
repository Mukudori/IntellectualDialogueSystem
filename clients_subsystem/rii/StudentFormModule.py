
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QPushButton, QComboBox
from clients_subsystem.rii.database.CathGroupModule import CathGroup
from clients_subsystem.rii.database.ClientModule import Client

class StudentForm (QWidget):
    def __init__(self, id=0, parent=0):
        super().__init__()
        self.initUI()
        self.ID = id
        self.Parent = parent
        if id:
            self.initEdit()
        else:
            self.setWindowTitle('Добавление нового студента')

    def initUI(self):
        self.lFio = QLabel('ФИО полностью')
        self.leFio = QLineEdit()
        self.lShort = QLabel('Фамилия И.О.')
        self.leShort = QLineEdit()
        hl1 = QHBoxLayout()
        hl1.addWidget(self.lFio)
        hl1.addWidget(self.leFio)
        mainL = QVBoxLayout()
        mainL.addLayout(hl1)

        hl2 =QHBoxLayout()
        hl2.addWidget(self.lShort)
        hl2.addWidget(self.leShort)
        mainL.addLayout(hl2)

        hl3 = QHBoxLayout()
        self.lGroup = QLabel('Группа')
        self.cbGroup = QComboBox()
        self.groupList = CathGroup().getList()
        self.cbGroup.addItems([rec['name'] for rec in self.groupList])
        hl3.addWidget(self.lGroup)
        hl3.addWidget(self.cbGroup)
        mainL.addLayout(hl3)

        self.pbSave = QPushButton('Сохранить')
        mainL.addWidget(self.pbSave)
        self.pbSave.clicked.connect(self.save)

        self.setLayout(mainL)


    def initEdit(self):
        rec = Client().getFromID(self.ID)
        self.leFio.setText(rec['fio'])
        self.leShort.setText(rec['shortfio'])
        for i in range(len(self.groupList)):
            if rec['idInfo'] == self.groupList[i]['id']:
                ind=i
        self.cbGroup.setCurrentIndex(ind)
        self.setWindowTitle('Редактирование информации о студенте')

    def save(self):
        fio = self.leFio.text()
        short = self.leShort.text()
        ind = self.cbGroup.currentIndex()
        idInfo = self.groupList[ind]['id']
        if self.ID:
            Client().updateStudent(idClient=self.ID, shortfio=self.leShort.text(),
                                   fio=fio, idInfo=idInfo)
        else:
            Client().insertStudent(fio=fio, shortfio=self.leShort.text(),
                                   idInfo=idInfo)
        if self.Parent:
            self.Parent.RefreshTable()
        self.close()