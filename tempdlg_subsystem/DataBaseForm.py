# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QMenu
from PyQt5 import uic, QtCore
#from tempdlg_subsystem.database import DataBaseModule
#from tempdlg_subsystem.EditDlgForm import EditDlgForm
from tempdlg_subsystem.database.ActionTableModule import ActionTable

from tempdlg_subsystem.database.AnswerTableModule import AnswerTable
from tempdlg_subsystem.database.QuestionTableModule import QuestionTable
from tempdlg_subsystem.EditActionForm import EditActionForm
from tempdlg_subsystem.database.UserGroupModule import UserGroupTable
from tempdlg_subsystem.database.ContextTableModule import ContextTable
from tempdlg_subsystem.EditUserGroupForm import EditUserGroup
from tempdlg_subsystem.EditContextModule import EditContextForm

class DataBaseForm(QMainWindow):
    
    def __init__(self):
        super(DataBaseForm,self).__init__()
        uic.loadUi("tempdlg_subsystem/ui/DataBaseForm.ui", self)
        self.InitMenu()

    def GetTableModel(self, table):
        

        if table == 'questiontab':
            model = QuestionTable().GetTableViewModel()
        elif table == 'answertab':
            model = AnswerTable().GetTableViewModel()
        elif table == 'actiontab':
            model = ActionTable().GetTableViewModel()
        elif table == 'usergrouptab':
            model = UserGroupTable().GetTableViewModel()
        elif table == 'contexttab':
            model = ContextTable().GetTableViewModel()
        #else:
           # model = DlgTable().GetViewModel()
        self.tableView.setModel(model)
        self.tableView.resizeRowsToContents()
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setStyleSheet("::section{Background-color:rgb(100,200,100);border-radius:14px;}")

    def RefreshTable(self):
       
        self.GetTableModel(self.GetTableName())

    def InitMenu(self):
        
        self.GetTableModel('questiontab')
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
        if(table == 'dlgtab'):
            self.EDF = EditDlgForm(id)
            self.EDF.show()
        elif (table == 'actiontab'):
            self.EAF = EditActionForm(id)
            self.EAF.show()
        elif (table == 'usergrouptab'):
            self.UGF = EditUserGroup(id)
            self.UGF.show()
        elif table == 'contexttab':
            self.ECT = EditContextForm(id)
            self.ECT.show()

    def OpenAddRecordForm(self):
        
        table = self.GetTableName()
        if (table == 'contexttab'):
            self.ECT = EditContextForm()
            self.ECT.show()
        elif (table == 'actiontab'):
            self.EAF = EditActionForm()
            self.EAF.show()
        elif table == 'usergrouptab':
            self.UGF = EditUserGroup()
            self.UGF.show()

    def DeleteRecord(self):
        id = self.GetSelectedRecordID()
        table = self.GetTableName()

        if (table == 'actiontab'):
            ActionTable().DeleteRecord(id)
        elif (table == 'contexttab'):
            ContextTable().CascadeDeleteFromID(id)
        elif table == 'usergrouptab':
            UserGroupTable().DeleteRecord(id)
        self.RefreshTable()

    def GetTableName(self):
        text = self.comboBox.currentText()
        if text == u'Вопросы':
            return 'questiontab'
        elif text == u'Ответы':
            return 'answertab'
        elif text == u'Диалоги общие':
            return 'dlgtab'
        elif text == u'Диалоги в контексте':
            return 'contexttab'
        elif text == u'Группы пользователей':
            return 'usergrouptab'
        return 'actiontab'





