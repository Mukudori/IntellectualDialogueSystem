from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QPushButton, QComboBox, QMessageBox

from clients_subsystem.rii.database.CathedraModule import Cathedra
from clients_subsystem.rii.database.ClientModule import Client
from clients_subsystem.rii.database.AuditoryModule import Auditory
from clients_subsystem.rii.database.TimeTableModule import TimeTable

class AddDisciplineForStudentsDialog(QWidget):
    def __init__(self, idGroup, numDay, tv):
        super().__init__()
        self.numDay = numDay
        self.tv = tv
        self.idGroup = idGroup
        self.initUI()
        self.connectSlots()

    def initUI(self):
        vLay = QVBoxLayout()
        hl1 = QHBoxLayout()
        self.lab1 = QLabel('Кафедра : ')
        self.cbCath = QComboBox()
        self.cathList = Cathedra().getList()
        self.cbCath.addItems([row['name'] for row in self.cathList])
        hl1.addWidget(self.lab1)
        hl1.addWidget(self.cbCath)
        vLay.addLayout(hl1)

        hl2 = QHBoxLayout()
        self.teachList = Client().getTeachersListFromIDCath(self.cathList[0]['id'])
        self.lab2 = QLabel('Преподаватель : ')
        self.cbTeacher = QComboBox()
        self.cbTeacher.addItems([row['shortfio'] for row in self.teachList])
        hl2.addWidget(self.lab2)
        hl2.addWidget(self.cbTeacher)
        vLay.addLayout(hl2)

        hl3 = QHBoxLayout()
        self.lab3 = QLabel('Аудитория : ')
        self.cbAud = QComboBox()
        self.audList = Auditory().getList()
        self.cbAud.addItems([row['num'] for row in self.audList])
        hl3.addWidget(self.lab3)
        hl3.addWidget(self.cbAud)
        vLay.addLayout(hl3)

        hl4 = QHBoxLayout()
        self.lab4 = QLabel('Дисциплина : ')
        self.leDis = QLineEdit()
        hl4.addWidget(self.lab4)
        hl4.addWidget(self.leDis)
        vLay.addLayout(hl4)

        hl5 = QHBoxLayout()
        self.lab5 = QLabel('Номер пары : ')
        self.cbNumLesson = QComboBox()
        self.cbNumLesson.addItems(['1','2','3','4','5','6'])
        hl5.addWidget(self.lab5)
        hl5.addWidget(self.cbNumLesson)
        vLay.addLayout(hl5)

        self.pbAdd = QPushButton('Добавить')
        vLay.addWidget(self.pbAdd)

        self.setLayout(vLay)
        self.setWindowTitle('Добавление дисциплины')

    def refreshTeachers(self):
        idC = self.cbCath.currentIndex()
        if idC==-1: idC=0
        self.teachList = Client().getTeachersListFromIDCath(
            idCath=self.cathList[idC]['id'])
        self.cbTeacher.clear()
        self.cbTeacher.addItems([row['shortfio'] for row in self.teachList])

    def getInsertData(self):
        idTeach = self.cbTeacher.currentIndex()
        if idTeach == -1:
            idTeach = self.teachList[0]['id']
        else:
            idTeach = self.teachList[idTeach]['id']
        idAud = self.cbAud.currentIndex()
        if idAud == -1:
            idAud = self.audList[0]['num']
        else:
            idAud = self.audList[idAud]['num']
        discipline = self.leDis.text()
        return (idTeach, idAud, discipline)


    def connectSlots(self):
        self.cbCath.currentIndexChanged.connect(self.refreshTeachers)

    def findLesson(self, numDay, numLesson, idGroup):
        pass


    def insertRecord(self):
        if not self.findLesson(numDay=self.numDay,
                               numLesson=self.cbNumLesson.currentText(),
                               idGroup=self.idGroup):
            idTeach, idAud, discipline = self.getInsertData()
            TimeTable().insertDiscipline(idTeacher=idTeach,
                                         idCathGroup=self.idGroup,
                                         discipline=discipline,
                                         numDay=self.numDay,
                                         numLesson=self.cbNumLesson.currentText(),
                                         idAud=idAud
                                         )
        else:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Ошибка")
            self.msg.setInformativeText("У этой группы уже стоит занятие "
                                        "этой парой.")
            self.msg.show()