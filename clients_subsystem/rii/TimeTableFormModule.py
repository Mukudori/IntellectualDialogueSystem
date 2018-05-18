
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu
from PyQt5 import uic, QtCore

from clients_subsystem.rii.database.ClientModule import Client
from clients_subsystem.rii.database.CathedraModule import Cathedra
from clients_subsystem.rii.TeacherFormModule import TeacherForm
from clients_subsystem.rii.StudentFormModule import StudentForm
from clients_subsystem.rii.database.CathGroupModule import CathGroup
from clients_subsystem.rii.database.TimeTableModule import TimeTable
from clients_subsystem.rii.AddDisciplineModule import \
    AddDisciplineDialog
from clients_subsystem.rii.DeleteDisciplineDialogModule import DeleteDialog


ClientsGroup = {'Students' : 3, 'Teachers' : 2}

class TimeTableForm(QMainWindow):
    def __init__(self, idClientsGroup, idClient, parent=0):
        super().__init__()
        uic.loadUi('clients_subsystem/rii/ui/TimeTableForm.ui', self)

        self.idClientsGroup = idClientsGroup
        self.idClient = idClient
        self.initTVTuple()
        if idClientsGroup == ClientsGroup['Teachers']:
            self.initTeacher()
        else:
            self.initStudents()
        if parent:
            parent.close()
        self.connectSlots()



    def initTeacher(self):
        self.lab1.setText('ФИО преподавателя : ')
        self.TeacherData = Client().getFromID(self.idClient)


        self.labFio.setText(self.TeacherData['fio'])
        self.labCath.setText(self.TeacherData['nameCath'])
        self.giveTVModel()

    def initStudents(self):
        self.GroupData = CathGroup().getFromID(self.idClient)
        self.lab1.setText('Группа : ')
        cathData = Cathedra().getRecord(id=self.GroupData['idCathedra'])
        self.labFio.setText(self.GroupData['name'])
        self.labCath.setText(cathData['name'])

        self.giveTVModel()


    def initTVTuple(self):
        self.TVs = (
            self.tv1,
            self.tv2,
            self.tv3,
            self.tv4,
            self.tv5,
            self.tv6,
            self.tv7,
            self.tv8,
            self.tv9,
            self.tv10,
            self.tv11,
            self.tv12
        )


    def giveTVModel(self, numDay=0):
        if numDay==0:
            if ClientsGroup['Students'] == self.idClientsGroup:
                for i in range(12):
                    model = TimeTable().getStudentsModel(idGroup=self.idClient, numDay=i+1)
                    self.TVs[i].setModel(model)
            else:
                for i in range(12):
                    model = TimeTable().getTeacherModel(idTeacher=self.idClient, numDay=i+1)
                    self.TVs[i].setModel(model)
        else:
            if ClientsGroup['Students'] == self.idClientsGroup:
                model = TimeTable().getStudentsModel(idGroup=self.idClient, numDay=numDay)
                self.TVs[numDay-1].setModel(model)
            else:
                model = TimeTable().getTeacherModel(idTeacher=self.idClient, numDay=numDay)
                self.TVs[numDay-1].setModel(model)

    def addDis(self, numDay):
        self.AddDis = AddDisciplineDialog(idClient=self.idClient,
                                          numDay=numDay,
                                          parent=self,
                                          idClientsGroup=self.idClientsGroup)
        self.AddDis.show()

    def delDis(self, numDay):
        self.DelDis = DeleteDialog(idClientsGroup=self.idClientsGroup,
                                   idClient=self.idClient,
                                   numDay=numDay,
                                   parent=self)
        self.DelDis.show()


    def createMenu(self, pos, numDay):
        def _add():
            self.addDis(numDay)

        def _del():
            self.delDis(numDay)


        actAdd = QAction(u'Добавить', self)
        actAdd.triggered.connect(_add)
        actDel = QAction(u'Удалить', self)
        actDel.triggered.connect(_del)

        menu = QMenu(self)
        menu.addAction(actAdd)
        menu.addAction(actDel)
        menu.exec_(self.sender().mapToGlobal(pos))

    def initCM1(self, pos):
        self.createMenu(pos=pos, numDay=1)
    def initCM2(self, pos):
        self.createMenu(pos=pos, numDay=2)
    def initCM3(self, pos):
        self.createMenu(pos=pos, numDay=3)
    def initCM4(self, pos):
        self.createMenu(pos=pos, numDay=4)
    def initCM5(self, pos):
        self.createMenu(pos=pos, numDay=5)
    def initCM6(self, pos):
        self.createMenu(pos=pos, numDay=6)
    def initCM7(self, pos):
        self.createMenu(pos=pos, numDay=7)
    def initCM8(self, pos):
        self.createMenu(pos=pos, numDay=8)
    def initCM9(self, pos):
        self.createMenu(pos=pos, numDay=9)
    def initCM10(self, pos):
        self.createMenu(pos=pos, numDay=10)
    def initCM11(self, pos):
        self.createMenu(pos=pos, numDay=11)
    def initCM12(self, pos):
        self.createMenu(pos=pos, numDay=12)

    def connectSlots(self):

        self.TVs[0].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TVs[0].customContextMenuRequested.connect(self.initCM1)

        self.TVs[1].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TVs[1].customContextMenuRequested.connect(self.initCM2)

        self.TVs[2].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TVs[2].customContextMenuRequested.connect(self.initCM3)

        self.TVs[3].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TVs[3].customContextMenuRequested.connect(self.initCM4)

        self.TVs[4].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TVs[4].customContextMenuRequested.connect(self.initCM5)

        self.TVs[5].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TVs[5].customContextMenuRequested.connect(self.initCM6)

        self.TVs[6].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TVs[6].customContextMenuRequested.connect(self.initCM7)

        self.TVs[7].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TVs[7].customContextMenuRequested.connect(self.initCM8)

        self.TVs[8].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TVs[8].customContextMenuRequested.connect(self.initCM9)

        self.TVs[9].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TVs[9].customContextMenuRequested.connect(self.initCM10)

        self.TVs[10].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TVs[10].customContextMenuRequested.connect(self.initCM11)

        self.TVs[11].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TVs[11].customContextMenuRequested.connect(self.initCM12)