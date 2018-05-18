from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QPushButton, QComboBox, QMessageBox

from clients_subsystem.rii.database.CathedraModule import Cathedra
from clients_subsystem.rii.database.ClientModule import Client
from clients_subsystem.rii.database.AuditoryModule import Auditory
from clients_subsystem.rii.database.TimeTableModule import TimeTable
from clients_subsystem.rii.database.CathGroupModule import CathGroup

ClientsGroup = {'Students' : 3, 'Teachers' : 2}


class AddDisciplineDialog(QWidget):
    def __init__(self, idClient, numDay, idClientsGroup, parent=0):
        super().__init__()

        self.numDay = numDay
        self.idClient =idClient
        self.idClientGroup = idClientsGroup
        self.Parent = parent
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

        self.lab2 = QLabel('Преподаватель : ')
        self.cbTeacherOrGroup = QComboBox()

        hl2.addWidget(self.lab2)
        hl2.addWidget(self.cbTeacherOrGroup)
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

    def initStudents(self):
        self.lab2.setText('Преподаватель : ')
        self.refreshTeachers()
        self.connectStudentSlots()

    def initTeacher(self):
        self.lab2.setText('Группа : ')
        self.refreshGroups()
        self.connectTeacherSlots()

    def refreshTeachers(self):
        idC = self.cbCath.currentIndex()
        if idC==-1: idC=0
        self.teachList = Client().getTeachersListFromIDCath(
            idCath=self.cathList[idC]['id'])
        self.cbTeacherOrGroup.clear()
        self.cbTeacherOrGroup.addItems([row['shortfio'] for row in self.teachList])

    def getInsertData(self):
        idTeachOrGroup = self.cbTeacherOrGroup.currentIndex()
        if idTeachOrGroup == -1:
            idTeachOrGroup = 0

        if self.idClientGroup == ClientsGroup['Students']:
            idTeachOrGroup = self.teachList[idTeachOrGroup]['id']
        else:
            idTeachOrGroup = self.groupList[idTeachOrGroup]['id']


        idAud = self.cbAud.currentIndex()
        if idAud == -1:
            idAud = self.audList[0]['id']
        else:
            idAud = self.audList[idAud]['id']
        discipline = self.leDis.text()
        return (idTeachOrGroup, idAud, discipline)

    def connectSlots(self):
        if self.idClientGroup == ClientsGroup['Students']:
            self.initStudents()
        else:
            self.initTeacher()


    def connectStudentSlots(self):
        self.cbCath.currentIndexChanged.connect(self.refreshTeachers)
        self.pbAdd.clicked.connect(self.insertRecord)

    def connectTeacherSlots(self):
        self.pbAdd.clicked.connect(self.insertRecord)
        self.cbCath.currentIndexChanged.connect(self.refreshGroups)

    def refreshGroups(self):
        idC = self.cbCath.currentIndex()
        if idC == -1: idC = 0
        self.groupList = CathGroup().getList(idCath=self.cathList[idC]['id'])
        self.cbTeacherOrGroup.clear()
        self.cbTeacherOrGroup.addItems([row['name'] for row in self.groupList])


    def findLesson(self, numDay, numLesson, idGroup, idTeacher):
        def _find(List):
            for row in List:
                if int(numLesson) == row['numLesson'] and row['discipline']!='-':
                    return True
            return False

        groupList = TimeTable().getGroupList(idGroup=idGroup, numDay=numDay)
        checkGroup = _find(groupList)
        if checkGroup:
            return (True, 'group')
        else:
            teachList = TimeTable().getTeacherList(idTeacher=idTeacher, numDay=numDay)
            checkTeacher = _find(teachList)
            if checkTeacher:
                return (True, 'teacher')


        return (False,0)


    def insertRecord(self):
        idTeachOrGroup, idAud, discipline = self.getInsertData()
        if self.idClientGroup == ClientsGroup['Students']:
            idGroup = self.idClient
            idTeacher = idTeachOrGroup
        else:
            idGroup = idTeachOrGroup
            idTeacher = self.idClient

        check = self.findLesson(numDay=self.numDay,
                               numLesson=self.cbNumLesson.currentText(),
                               idGroup=idGroup,
                               idTeacher=idTeacher)
        if not check[0]:
            TimeTable().insertDiscipline(idTeacher=idTeacher,
                                         idCathGroup=idGroup,
                                         discipline=discipline,
                                         numDay=self.numDay,
                                         numLesson=self.cbNumLesson.currentText(),
                                         idAud=idAud
                                         )

            if self.Parent:
                self.Parent.giveTVModel(self.numDay)
            self.close()
        else:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setText("Ошибка")
            if check[1]=='group':
                text = "У этой группы пара занята."
            else:
                text = "У этого преподавателя пара занята."
            self.msg.setInformativeText(text)
            self.msg.show()