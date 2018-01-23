from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import uic, QtCore
from database import DataBaseModule


class EditDataBaseForm(QWidget):
    '''Форма Редактирования диалога'''
    def __init__(self, id):
        super().__init__()
        uic.loadUi("EditDialogForm.ui", self)
        self.ID = id
        self.ModelQ = QStandardItemModel()
        self.ModelA = QStandardItemModel()
        self.pbAddQuestion.clicked.connect(self.__AddLineQ)
        self.pbDelQuestion.clicked.connect(self.__DelLineQ)
        self.pbAddAnswer.clicked.connect(self.__AddLineA)
        self.pbDelAnswer.clicked.connect(self.__DelLineA)
        self.getRecord(id)

    def getRecord(self, id):
        sql1 = 'SELECT question FROM dialogtab where id = \''+id+'\''
        sql2 = 'SELECT answer FROM dialogtab where id = \'' + id + '\''
        sqlAct = '''SELECT actiontab.action FROM dialogtab INNER JOIN actiontab 
        ON  dialogtab.action = actiontab.id WHERE dialogtab.id = \'''' + id + '\''

        self.ModelQ = self.__CreateModel(sql1,'question')
        self.ModelA = self.__CreateModel(sql2,'answer')
        self.tvQuestion.setModel(self.ModelQ)
        self.tvAnswer.setModel(self.ModelA)
        self.label.setText("Реакция на вопрос :" + str(DataBaseModule.GetData(sqlAct)[0]['action']))

    def __CreateModel(self, sql, field):
        data = DataBaseModule.GetData(sql)
        model = QStandardItemModel()
        horhead = list(data[0].keys())
        model.setHorizontalHeaderLabels(['Строка','Код'])

        Text = data[0][field].split(';')

        for i in range(len(Text)):
            if Text[i] != ['']:
                item = QStandardItemModel()

                wt = WordTableModule.WordTable()
                item = QStandardItem(wt.GetDecodeText(Text[i]))
                model.setItem(i-1, 0, item)

                item = QStandardItem(Text[i])
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                model.setItem(i-1, 1, item)
        return model

    def __AddLineQ(self):
        lastRow = self.ModelQ.rowCount()
        self.ModelQ.insertRow(lastRow)
        self.ModelQ.setData(self.ModelQ.index(lastRow,0),'')
        self.ModelQ.setData(self.ModelQ.index(lastRow, 1), '')
        self.tvQuestion.selectRow(lastRow)
        self.tvQuestion.setFocus()


    def __DelLineQ(self):
        selectModel = self.tvQuestion.selectionModel()
        indexes = selectModel.selectedIndexes()

        for index in indexes:
            row = index.row()
            if not self.ModelQ.removeRow(row):
                print (self.ModelQ.lastError.text())
            else:
                self.tvQuestion.setModel(self.ModelQ)

    def __AddLineA(self):
        lastRow = self.ModelA.rowCount()
        self.ModelA.insertRow(lastRow)
        self.ModelA.setData(self.ModelA.index(lastRow,0),'')
        self.ModelA.setData(self.ModelA.index(lastRow, 1), '')
        self.tvAnswer.selectRow(lastRow)
        self.tvAnswer.setFocus()

    def __DelLineA(self):
        selectModel = self.tvAnswer.selectionModel()
        indexes = selectModel.selectedIndexes()

        for index in indexes:
            row = index.row()
            self.ModelA.removeRow(row)
            self.tvAnswer.setModel(self.ModelA)