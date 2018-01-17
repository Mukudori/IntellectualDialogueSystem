from PyQt5.QtWidgets import QWidget, QAction, QMenu
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import uic, QtCore, QtSql


import DataBase

#Форма базы данных
class DataBaseForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("DataBaseForm.ui", self)
        self.GetTableModel('wordsgrouptab','id;semantic')
        self.comboBox.currentIndexChanged.connect(self.RefreshTable)
        self.InitContextMenu()

    #Вывод модели таблицы
    def GetTableModel(self, table, header):
        db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
        db.setHostName("localhost")
        db.setDatabaseName("botdb")
        db.setUserName("root")
        db.setPassword("4862159357")

        model = QtSql.QSqlTableModel
        model.set
        model.setTable(table)
        model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit);
        data = DataBase.GetTable("SELECT * FROM "+table)
        horhead=header.split(';')
        self.label_2.setText('Поиск по ' + horhead[1] + ' :')
        verhead = []
        model.setHorizontalHeaderLabels(horhead)
        for i in range(len(data)):
            verhead.append(str(''))
        model.setVerticalHeaderLabels(verhead)

        for i in range(len(verhead)):
            for j in range(len(horhead)):
                item = QStandardItemModel()
                if table == 'dialogtab' and (horhead[j] == 'question' or horhead[j] == 'answer'):
                    item = QStandardItem(self.GetTextFromCodes(data[i][horhead[j]]))
                else:
                    item = QStandardItem(str(data[i][horhead[j]]))
                model.setItem(i,j,item)
        self.tableView.setModel(model)
        self.tableView.resizeRowsToContents()
        self.tableView.resizeColumnsToContents()

    #Обновить таблицу
    def RefreshTable(self):
        ind = self.comboBox.currentIndex()
        if ind == 0:
            self.GetTableModel('wordsgrouptab', 'id;semantic')
        elif ind == 1:
            self.GetTableModel('wordtab', 'id;word;idGroup')
        elif ind == 2:
            self.GetTableModel('dialogtab', 'id;question;answer;action')
        elif ind == 3:
            self.GetTableModel('actiontab', 'id;action;note')

    #Преобразовать закодированную строку в текст
    def GetTextFromCodes(self, codeText):
        codeStr = codeText.split(';')
        outS = str()
        for s in codeStr:
            wordid = s.split(' ')
            if wordid != ['']:
                for word in wordid:
                    data = DataBase.GetTable("select word from wordtab"+
                    " where idGroup='"+word.split('-')[0]+
                    "' and id='"+word.split('-')[1]+"'")
                    outS=outS+data[0]['word']+' '
                outS = outS + ';'
        return outS

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