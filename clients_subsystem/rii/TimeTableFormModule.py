
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu
from PyQt5 import uic, QtCore

from clients_subsystem.rii.database.ClientModule import Client
from clients_subsystem.rii.database.CathedraModule import Cathedra
from clients_subsystem.rii.TeacherFormModule import TeacherForm
from clients_subsystem.rii.StudentFormModule import StudentForm
from clients_subsystem.rii.database.CathGroupModule import CathGroup
from clients_subsystem.rii.database.TimeTableModule import TimeTable
from clients_subsystem.rii.AddDisciplineForStudentsModule import \
    AddDisciplineForStudentsDialog



class TimeTableForm(QMainWindow):
    def __init__(self, idClientsGroup, idClient, parent=0):
        super().__init__()
        uic.loadUi('clients_subsystem/rii/ui/TimeTableForm.ui', self)
        self.Group = {'Students' : 3, 'Teachers' : 2}
        self.idClientsGroup = idClientsGroup
        self.idClient = idClient
        self.initTVTuple()
        if idClientsGroup == self.Group['Teachers']:
            self.initTeacher()
        else:
            self.initStudents()
        self.giveTVModel(1)
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
        groupID = Client().getFromID(self.idClient)['idInfo']
        self.GroupData = CathGroup().getFromID(groupID)
        self.lab1.setText('Группа : ')
        self.labFio.setText(self.GroupData['name'])

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
            if self.Group['Students'] == self.idClientsGroup:
                for i in range(12):
                    model = TimeTable().getStudentsModel(idGroup=self.idClient, numDay=i+1)
                    self.TVs[i].setModel(model)
            else:
                for i in range(12):
                    model = TimeTable().getTeacherModel(idTeacher=self.idClient, numDay=i+1)
                    self.TVs[i].setModel(model)


    def getSelectedRecordID(self, tv):
        currentDiscount = tv.currentIndex()
        id = self.tableView.model().data(self.tableView.model().index(currentDiscount.row(), 0), 0)
        if id:
            return int(id)
        else:
            return 0

    def initCM1(self, pos):

        def add_1():
            self.AddDis = AddDisciplineForStudentsDialog(idGroup=self.idClient,
                                                         numDay=1,
                                                         tv = self.TVs[0])
            self.AddDis.show()

        def del_1():
            id = self.getSelectedRecordID(self.TVs[0])
            TimeTable.deleteDiscipline(id)

        actAdd1 = QAction(u'Добавить', self)
        actAdd1.triggered.connect(add_1)
        actDel1 = QAction(u'Удалить', self)
        actDel1.triggered.connect(del_1)

        menu1 = QMenu(self)
        menu1.addAction(actAdd1)
        menu1.addAction(actDel1)
        menu1.exec_(self.sender().mapToGlobal(pos))



    def showDialog(self):
        pass

    def connectSlots(self):
        self.TVs[0].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TVs[0].customContextMenuRequested.connect(self.initCM1)