# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu
from PyQt5 import uic, QtCore

from clients_subsystem.rii.database.ClientModule import Client
from clients_subsystem.rii.database.CathedraModule import Cathedra
from clients_subsystem.rii.TeacherFormModule import TeacherForm
from clients_subsystem.rii.StudentFormModule import StudentForm
from clients_subsystem.rii.database.CathGroupModule import CathGroup
from clients_subsystem.rii.CathGroupFormModule import CathGroupForm
from clients_subsystem.rii.CathedraFormModule import CathedraForm
from clients_subsystem.rii.OpenTimeTableModule import OpenTimeTableForm
from clients_subsystem.rii.database.AuditoryModule import Auditory
from clients_subsystem.rii.AddAuditoryDialogModule import AddAuditoryDialog
from clients_subsystem.rii.EditClientFormModule import EditClientForm

class RIIDataBaseForm(QMainWindow):
    
    def __init__(self):
        super().__init__()
        uic.loadUi("clients_subsystem/rii/ui/DataBaseForm.ui", self)
        self.AdisTable = {'None': 0, 'Cathedra': 1, 'Group' : 2 }

        self.InitMenu()


    def GetTableModel(self, table):

        if table == 'Студенты':
            self.setVisibleCB(True)
            if self.selectedTable != self.AdisTable['Group']:
                self.cbGroupInit()
            idGroup = self.getAdditionalParIndex()
            model = Client().getTVStudentsModel(idGroup)
        elif table == 'Преподаватели':
            self.setVisibleCB(True)
            if self.selectedTable != self.AdisTable['Cathedra']:
                self.cbCathedraInit()
            idCathedra = self.getAdditionalParIndex()
            model = Client().getTVTeachersModel(idCathedra)
        elif table == 'Кафедры':
            self.setVisibleCB(False)
            model = Cathedra().getTVCathedraModel(zav=False)
        elif table == 'Группы студентов':
            self.setVisibleCB(True)
            if self.selectedTable != self.AdisTable['Cathedra']:
                self.cbCathedraInit()
            idCathedra = self.getAdditionalParIndex()
            model = CathGroup().getTVCathGroup(idCathedra)
        elif table == 'Аудитории':
            self.setVisibleCB(False)
            model = Auditory().getTVModel()


        self.tableView.setModel(model)
        self.tableView.resizeRowsToContents()
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setStyleSheet("::section{Background-color:rgb(100,200,100);border-radius:14px;}")

    def RefreshTable(self):
       
        self.GetTableModel(self.GetTableName())

    def InitMenu(self):
        self.slotConnected = False
        self.selectedTable = 0
        self.connect_disconnect_ViewSlot()

        self.GetTableModel('Студенты')

        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.moreInfoAct = QAction(u'Редактировать запись', self)
        self.moreInfoAct.triggered.connect(self.OpenEditRecordForm)
        self.deleteRecordAct = QAction(u'Удалить запись', self)
        self.deleteRecordAct.triggered.connect(self.DeleteRecord)

        self.connectSlots()


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
            self.Teacher = TeacherForm(id,parent=self)
            self.Teacher.show()
        elif table=='Студенты':
            self.Student = StudentForm(id, parent=self)
            self.Student.show()
        elif table=='Группы студентов':
            self.CathGroup = CathGroupForm(id=id, parent=self)
            self.CathGroup.show()
        elif table == 'Кафедры':
            self.Cathedra = CathedraForm(id=id, parent = self)
            self.Cathedra.show()


    def OpenAddRecordForm(self):
        
        table = self.GetTableName()
        if table == 'Преподаватели':
            self.Teacher = TeacherForm(parent=self)
            self.Teacher.show()
        elif table=='Студенты':

            self.Student = StudentForm(parent=self)
            self.Student.show()
        elif table=='Группы студентов':
            self.CathGroup = CathGroupForm(parent=self)
            self.CathGroup.show()
        elif table == 'Кафедры':
            self.Cathedra = CathedraForm(parent=self)
            self.Cathedra.show()
        elif table == 'Аудитории':
            self.AuditInsert = AddAuditoryDialog(parent = self)
            self.AuditInsert.show()

    def DeleteRecord(self):
        id = self.GetSelectedRecordID()
        if id:
            table = self.GetTableName()

            if (table == 'Преподаватели'):
                Client().deleteTeacher(id)
            elif table == "Аудитории":
                Auditory().deleteRecord(id)

            self.RefreshTable()

    def GetTableName(self):
        text = self.comboBox.currentText()
        return text

    def cbCathedraInit(self):

        self.selectedTable = self.AdisTable['Cathedra']
        self.connect_disconnect_ViewSlot()
        self.setVisibleCB(True)
        self.lView.setText("Кафедра :")
        self.CathList = Cathedra().getList()
        self.cbView.clear()
#        itemList =
        for line in self.CathList:
            self.cbView.addItem(line['name'])
        self.connect_disconnect_ViewSlot()

    def cbGroupInit(self):

        self.selectedTable = self.AdisTable['Group']
        self.connect_disconnect_ViewSlot()
        self.setVisibleCB(True)
        self.lView.setText("Группа :")
        self.CathGroupList = CathGroup().getList()
        self.cbView.clear()
        for line in self.CathGroupList:
            self.cbView.addItem(line['name'])
        self.connect_disconnect_ViewSlot()

    def setVisibleCB(self, val):
        self.lView.setVisible(val)
        self.cbView.setVisible(val)
        self.cbView.update()

    def connect_disconnect_ViewSlot(self):
        if self.slotConnected:
            self.slotConnected=False
            self.cbView.currentIndexChanged.disconnect(self.RefreshTable)
        else:
            self.slotConnected = True
            self.cbView.currentIndexChanged.connect(self.RefreshTable)

    def getAdditionalParIndex(self):
        if self.selectedTable == self.AdisTable['Cathedra']:
            id = self.CathList[self.cbView.currentIndex()]['id']
            return id
        elif self.selectedTable == self.AdisTable['Group']:
            id = self.CathGroupList[self.cbView.currentIndex()]['id']
            return id
        else:
            return 0

    def openTimeTable(self):
        self.openTT = OpenTimeTableForm()
        self.openTT.show()

    def connectSlots(self):
        self.comboBox.currentIndexChanged.connect(self.RefreshTable)
        self.tableView.customContextMenuRequested.connect(self.RunContextMenu)
        self.addRecord.triggered.connect(self.OpenAddRecordForm)
        self.editRecord.triggered.connect(self.OpenEditRecordForm)
        self.delRecord.triggered.connect(self.DeleteRecord)

        self.refreshView.triggered.connect(self.RefreshTable)
        self.delRecord.triggered.connect(self.DeleteRecord)

        self.actTimeTable.triggered.connect(self.openTimeTable)
        self.act_AddClient.triggered.connect(self.AddClient)

    def AddClient(self):
        self.EditClient = EditClientForm()
        self.EditClient.show()