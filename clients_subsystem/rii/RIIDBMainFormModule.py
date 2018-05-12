# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu
from PyQt5 import uic, QtCore

from clients_subsystem.rii.database.ClientModule import Client
from clients_subsystem.rii.database.CathedraModule import Cathedra
from clients_subsystem.rii.TeacherFormModule import TeacherForm
from clients_subsystem.rii.StudentFormModule import StudentForm
from clients_subsystem.rii.database.CathGroupModule import CathGroup
from clients_subsystem.rii.CathGroupFormModule import CathGroupForm

class RIIDataBaseForm(QMainWindow):
    
    def __init__(self):
        super().__init__()
        uic.loadUi("clients_subsystem/rii/ui/DataBaseForm.ui", self)
        self.InitMenu()

    def GetTableModel(self, table):

        if table == 'Студенты':
            model = Client().getTVStudentsModel()
        elif table == 'Преподаватели':
            model = Client().getTVTeachersModel()
        elif table == 'Кафедры':
            model = Cathedra().getTVCathedraModel()
        elif table == 'Группы студентов':
            model = CathGroup().getTVCathGroup()


        self.tableView.setModel(model)
        self.tableView.resizeRowsToContents()
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setStyleSheet("::section{Background-color:rgb(100,200,100);border-radius:14px;}")

    def RefreshTable(self):
       
        self.GetTableModel(self.GetTableName())

    def InitMenu(self):
        
        self.GetTableModel('Студенты')
        self.comboBox.currentIndexChanged.connect(self.RefreshTable)
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.RunContextMenu)

        self.moreInfoAct = QAction(u'Редактировать запись', self)
        self.moreInfoAct.triggered.connect(self.OpenEditRecordForm)
        self.deleteRecordAct = QAction(u'Удалить запись', self)
        self.deleteRecordAct.triggered.connect(self.DeleteRecord)

        self.addRecord.triggered.connect(self.OpenAddRecordForm)
        self.editRecord.triggered.connect(self.OpenEditRecordForm)
        self.delRecord.triggered.connect(self.DeleteRecord)

        self.refreshView.triggered.connect(self.RefreshTable)
        self.delRecord.triggered.connect(self.DeleteRecord)

        self.setWindowTitle('База данных РИИ')

    def RunContextMenu(self, pos):
        
        menu = QMenu(self)
        menu.addAction(self.moreInfoAct)
        menu.addAction(self.deleteRecordAct)
        menu.exec_(self.sender().mapToGlobal(pos))

    def GetSelectedRecordID(self):
        currentDiscount = self.tableView.currentIndex()
        id = self.tableView.model().data(self.tableView.model().index(currentDiscount.row(), 0), 0)
        if id:
            return int(id)
        else:
            return 0

    def OpenEditRecordForm(self):
        
        id=self.GetSelectedRecordID()
        table = self.GetTableName()
        if(table == 'Преподаватели'):
            self.Teacher = TeacherForm(id)
            self.Teacher.show()
        elif table=='Студенты':
            self.Student = StudentForm(id)
            self.Student.show()
        elif table=='Группы студентов':
            self.CathGroup = CathGroupForm(id=id, parent=self)
            self.CathGroup.show()


    def OpenAddRecordForm(self):
        
        table = self.GetTableName()
        if table == 'Преподаватели':
            self.Teacher = TeacherForm()
            self.Teacher.show()
        elif table=='Студенты':
            self.Student = StudentForm()
            self.Student.show()
        elif table=='Группы студентов':
            self.CathGroup = CathGroupForm(parent=self)
            self.CathGroup.show()

    def DeleteRecord(self):
        id = self.GetSelectedRecordID()
        if id:
            table = self.GetTableName()

            if (table == 'Преподаватели'):
                table = Client()
                table.deleteTeacher(id)

            self.RefreshTable()

    def GetTableName(self):
        text = self.comboBox.currentText()
        return text





