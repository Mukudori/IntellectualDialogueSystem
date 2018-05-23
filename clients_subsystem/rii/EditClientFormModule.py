

from clients_subsystem.rii.database.CathGroupModule import CathGroup
from clients_subsystem.rii.database.ClientModule import Client
from clients_subsystem.rii.database.CathedraModule import Cathedra
from tempdlg_subsystem.database.ClientTabModule import ClientsTab
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QPushButton, QComboBox


class EditClientForm (QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initClientsGroup()
        self.initCath()
        self.initStudents()
        self.connectSlots()


    def initUI(self):
        vLay = QVBoxLayout()

        h1 = QHBoxLayout()

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
        self.clientGroupList = [{'name' : 'Студент', 'id': 3},
                                {'name': 'Преподаватель', 'id': 2},
                                {'name': 'Администратор', 'id': 1}
                                ]
        self.cbClientGroup.addItems([row['name'] for row in self.clientGroupList])


    def initCath(self):
        self.cathList = Cathedra().getList()
        self.cbCath.clear()
        self.cbCath.addItems([row['name'] for row in self.cathList])


    def _getCathID(self):
        ind = self.cbCath.currentIndex()
        if ind == -1:
            ind = 0

        return self.cathList[ind]['id']

    def initStudents(self):
        self.setVisibleOtherCB(True)
        idCath = self._getCathID()

        self.labClient.setText('Группа')
        self.studentList = CathGroup().getList(idCath=idCath)
        self.cbClient.clear()
        self.cbClient.addItems([row['name'] for row in self.studentList])



    def initTeachers(self):
        self.setVisibleOtherCB(True)
        idCath = self._getCathID()
        self.labClient.setText('ФИО')
        self.teacherList = Client().getTeachersListFromIDCath(idCath=idCath)
        self.cbClient.clear()
        self.cbClient.addItems([row['shortfio'] for row in self.teacherList])

    def setVisibleOtherCB(self, val):
        self.lab2.setVisible(val)
        self.cbCath.setVisible(val)
        self.labClient.setVisible(val)
        self.cbClient.setVisible(val)

    def initAdmin(self):
        self.setVisibleOtherCB(False)

    def refreshClient(self):

        def getCurID():
            curInd = self.cbClientGroup.currentIndex()
            if curInd == -1:
                curInd = 0
            return self.clientGroupList[curInd]['id']

        text = self.cbClientGroup.currentText()
        if text == "Администратор":
            self.initAdmin()
        elif text == "Преподаватель":
            self.initTeachers()
        elif text == "Студент":
            self.initStudents()

    def connectSlots(self):
        self.cbClientGroup.currentIndexChanged.connect(self.refreshClient)
        self.cbCath.currentIndexChanged.connect(self.refreshClient)
        self.pb.clicked.connect(self.save)

    def initEdit(self):
        pass

    def insertAdmin(self):
        idTele = self.leTelegram.text()
        ClientsTab().insertClient(idClient=1,
                                  idClientGroup=1,
                                  idTelegram=idTele)


    def insertStudent(self):
        idTele = self.leTelegram.text()
        inC = self.cbClient.currentIndex()
        if inC == -1:
            inC = 0
        inC = self.studentList[inC]['id']
        ClientsTab().insertClient(idClient=inC,
                                  idClientGroup=3,
                                  idTelegram=idTele
                                  )

    def insertTeacher(self):
        idTele = self.leTelegram.text()
        inC = self.cbClient.currentIndex()
        if inC == -1:
            inC = 0
        inC = self.teacherList[inC]['id']
        ClientsTab().insertClient(idClient=inC,
                                  idClientGroup=2,
                                  idTelegram=idTele
                                  )

    def insertRecord(self, text):
        if text == 'Администратор':
            self.insertAdmin()
        elif text == "Студент":
            self.insertStudent()
        elif text == 'Преподаватель':
            self.insertTeacher()


    def save(self):
        text = self.cbClientGroup.currentText()
        self.insertRecord(text)
        self.close()