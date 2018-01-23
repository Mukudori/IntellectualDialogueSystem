from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QMenu
from PyQt5 import uic, QtCore
from database import DataBaseModule
import EditDlgForm
from database.ActionTableModule import ActionTable
from database.DlgTableModule import  DlgTable
from database.AnswerTableModule import AnswerTable
from database.QuestionTableModule import QuestionTable

class DataBaseForm(QMainWindow):
    '''Форма базы данных.
    Показывает содержимое таблиц, откуда можно перейти на форму редактирования запси
    '''
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/DataBaseForm.ui", self)
        self.InitMenu()

    def GetTableModel(self, table):
        '''Вывод модели таблицы'''

        if table == 'questiontab':
            model = QuestionTable().GetTableViewModel()
        elif table == 'answertab':
            model = AnswerTable().GetTableViewModel()
        elif table == 'actiontab':
            model = ActionTable().GetTableViewModel()
        else:
            model = DlgTable().GetViewModel()
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

        self.addRecord.triggered.connect(self.OpenAddRecordForm)
        self.editRecord.triggered.connect(self.OpenEditRecordForm)
        self.delRecord.triggered.connect(self.DeleteRecord)

    def RunContextMenu(self, pos):
        '''Запуск контекстного меню'''
        menu = QMenu(self)
        menu.addAction(self.moreInfoAct)
        menu.addAction(self.deleteRecordAct)
        menu.exec_(self.sender().mapToGlobal(pos))

    def OpenEditRecordForm(self):
        '''Открывает форму редактирования'''
        currentDiscount = self.tableView.currentIndex()
        id = self.tableView.model().data(self.tableView.model().index(currentDiscount.row(), 0), 0)
        if(self.GetTableName() == 'dlgtab'):
            self.EDF = EditDlgForm.EditDlgForm(id)
            self.EDF.show()

    def OpenAddRecordForm(self):
        '''Открывает форму добавления'''
        if (self.GetTableName() == 'dlgtab'):
            self.EDF = EditDlgForm.EditDlgForm(0)
            self.EDF.show()

    def DeleteRecord(self):
        pass

    def GetTableName(self):
        text = self.comboBox.currentText()
        if text == 'Вопросы':
            return 'questiontab'
        elif text == 'Ответы':
            return 'answertab'
        elif text == 'Диалоги':
            return 'dlgtab'
        return 'actiontab'

