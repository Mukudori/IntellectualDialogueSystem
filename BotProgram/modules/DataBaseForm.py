from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QMenu
from PyQt5 import uic, QtCore
from modules.database import DataBaseModule
#from modules.EditDlgForm import EditDlgForm
from modules.database.ActionTableModule import ActionTable
#from modules.database.DlgTableModule import  DlgTable
from modules.database.AnswerTableModule import AnswerTable
from modules.database.QuestionTableModule import QuestionTable
from modules.EditActionForm import EditActionForm
from modules.database.UserGroupModule import UserGroupTable
from modules.database.ContextTableModule import ContextTable
from modules.EditUserGroupForm import EditUserGroup
from modules.EditContextModule import EditContextForm

class DataBaseForm(QMainWindow):
    '''Форма базы данных.
    Показывает содержимое таблиц, откуда можно перейти на форму
    редактирования запси
    '''
    def __init__(self):
        super().__init__()
        uic.loadUi("modules/ui/DataBaseForm.ui", self)
        self.InitMenu()

    def GetTableModel(self, table):
        '''Вывод модели таблицы'''

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
        '''Обновить таблицу '''
        self.GetTableModel(self.GetTableName())

    def InitMenu(self):
        '''инициализация меню'''
        self.GetTableModel('questiontab')
        self.comboBox.currentIndexChanged.connect(self.RefreshTable)
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.RunContextMenu)

        self.moreInfoAct = QAction('Редактировать запись', self)
        self.moreInfoAct.triggered.connect(self.OpenEditRecordForm)
        self.deleteRecordAct = QAction('Удалить запись', self)
        self.deleteRecordAct.triggered.connect(self.DeleteRecord)

        self.addRecord.triggered.connect(self.OpenAddRecordForm)
        self.editRecord.triggered.connect(self.OpenEditRecordForm)
        self.delRecord.triggered.connect(self.DeleteRecord)

        self.refreshView.triggered.connect(self.RefreshTable)
        self.delRecord.triggered.connect(self.DeleteRecord)

    def RunContextMenu(self, pos):
        '''Запуск контекстного меню'''
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
        '''Открывает форму редактирования'''
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
        '''Открывает форму добавления'''
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
        if text == 'Вопросы':
            return 'questiontab'
        elif text == 'Ответы':
            return 'answertab'
        elif text == 'Диалоги общие':
            return 'dlgtab'
        elif text == 'Диалоги в контексте':
            return 'contexttab'
        elif text == 'Группы пользователей':
            return 'usergrouptab'
        return 'actiontab'





