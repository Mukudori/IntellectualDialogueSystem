from PyQt5.QtWidgets import QWidget, QAction, QMenu
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import uic, QtCore, QtSql


import DataBase

#Форма базы данных
class DataBaseForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("DataBaseForm.ui", self)
        self.GetTableModel('wordsgrouptab')
        self.comboBox.currentIndexChanged.connect(self.RefreshTable)


    #Вывод модели таблицы
    def GetTableModel(self, table):
        self.tableView.setModel(DataBase.GetTableViewModel("select * from " +table))
        self.tableView.resizeRowsToContents()
        self.tableView.resizeColumnsToContents()

    #Обновить таблицу
    def RefreshTable(self):
        '''ind = self.comboBox.currentIndex()
        if ind == 0:
            self.GetTableModel('wordsgrouptab')
        elif ind == 1:
            self.GetTableModel('wordtab')
        elif ind == 2:
            self.GetTableModel('dialogtab')
        elif ind == 3:
            self.GetTableModel('actiontab')
          '''
        self.GetTableModel(self.comboBox.currentText())



    def InitContextMenu(self):
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.RunContextMenu)

        self.moreInfoAct = QAction('Подробнее', self)
        self.moreInfoAct.triggered.connect(self.OpenMoreInfoForm)
        self.deleteRecordAct =QAction('Удалить запись', self)
       # self.deleteRecordAct.triggered.connect(self.DeleteRecord)

    def RunContextMenu(self, pos):
        menu = QMenu(self)
        menu.addAction(self.moreInfoAct)
        menu.addAction(self.deleteRecordAct)
        menu.exec_(self.sender().mapToGlobal(pos))

    def OpenMoreInfoForm(self):
        selectModel = self.tableView.selectionModel()
        if (selectModel.hasSelection()):
            self.lineEdit.setText(str(selectModel.selectedRows().row()))
