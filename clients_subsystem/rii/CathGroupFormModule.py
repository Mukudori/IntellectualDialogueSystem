from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QPushButton, QComboBox
from clients_subsystem.rii.database.CathGroupModule import CathGroup
from clients_subsystem.rii.database.ClientModule import Client
from clients_subsystem.rii.database.CathedraModule import Cathedra

class CathGroupForm(QWidget):
    def __init__(self, id=0, parent=0):
        super().__init__()
        self.ID = id
        self.Parent = parent
        self.initUI()
        if id:
            self.initEdit()

    def initUI(self):
        vLay = QVBoxLayout()
        hl1=QHBoxLayout()
        self.lName = QLabel('Наименование')
        self.leName = QLineEdit()
        hl1.addWidget(self.lName)
        hl1.addWidget(self.leName)
        vLay.addLayout(hl1)

        self.lCath = QLabel('Кафедра')
        self.cbCath = QComboBox()
        self.cathList = Cathedra().getList()
        self.cbCath.addItems([rec['name'] for rec in self.cathList])
        hl2 = QHBoxLayout()
        hl2.addWidget(self.lCath)
        hl2.addWidget(self.cbCath)
        vLay.addLayout(hl2)

        hl3 = QHBoxLayout()
        self.lTeacher = QLabel('Куратор')
        self.cbTeacher = QComboBox()
        hl3.addWidget(self.lTeacher)
        hl3.addWidget(self.cbTeacher)
        vLay.addLayout(hl3)

        hl4 = QHBoxLayout()
        self.lCourse = QLabel('Курс')
        self.leCourse = QLineEdit()
        hl4.addWidget(self.lCourse)
        hl4.addWidget(self.leCourse)
        vLay.addLayout(hl4)

        self.pbSave = QPushButton('Сохранить')
        vLay.addWidget(self.pbSave)
        self.setLayout(vLay)

        self.pbSave.clicked.connect(self.save)
        self.cbCath.currentIndexChanged.connect(self.refreshTeachers)

        self.setWindowTitle('Добавление новой группы')
        self.refreshTeachers()

    def initEdit(self):
        record = CathGroup().getFromID(self.ID)
        self.leName.setText(record['name'])
        for i in range(len(self.cathList)):
            if record['idCathedra'] == self.cathList[i]['id']:
                ind = i
                break
        self.cbCath.setCurrentIndex(ind)
        self.refreshTeachers()
        for i in range(len(self.teachersList)):
            if record['idCurator'] == self.teachersList[i]['id']:
                indT = i
                break
        self.cbTeacher.setCurrentIndex(indT)
        self.leCourse.setText(record['course'])


        self.setWindowTitle('Редактирование зиписи')

    def refreshTeachers(self):
        cbi = self.cbCath.currentIndex()
        idCath = self.cathList[cbi]['id']
        self.teachersList = Client().getTeachersListFromIDCath(idCath=idCath)
        self.cbTeacher.clear()
        self.cbTeacher.addItems([rec['shortfio'] for rec in self.teachersList])

    def insertRecord(self):
        idC = self.cathList[self.cbCath.currentIndex()]['id']
        idT = self.teachersList[self.cbTeacher.currentIndex()]['id']
        CathGroup().insertRecord(name=self.leName.text(),
                                 idCath=idC,
                                 idTeacher=idT,
                                 course=self.leCourse.text())

    def updateRecord(self):
        idC = self.cathList[self.cbCath.currentIndex()]['id']
        idT = self.teachersList[self.cbTeacher.currentIndex()]['id']
        CathGroup().updateRecord(id = self.ID,
                                 name=self.leName.text(),
                                 idCath=idC,
                                 idTeacher=idT,
                                 course=self.leCourse.text())

    def save(self):
        if self.ID:
            self.updateRecord()
        else:
            self.insertRecord()

        if self.Parent:
            self.Parent.RefreshTable()

        self.close()




