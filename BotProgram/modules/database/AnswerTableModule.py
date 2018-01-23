from database import DataBaseModule
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore

class AnswerTable:

    def __init__(self):
        self.__Table = DataBaseModule.GetData('SELECT * FROM answertab')

    def GetAllData(self):
        return self.__Table

    def GetDataFromID(self,id):
        pass
    def GetAnswerFromID(self,id):
        for record in self.__Table:
            if record['id']==id: return record['answer']
        return 0

    def GetTableViewModel(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['id', 'Ответ'])
        model.setVerticalHeaderLabels([' '] * len(self.__Table))

        for i in range(len(self.__Table)):
            item = QStandardItem(str(self.__Table[i]['id']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 0, item)

            item = QStandardItem(str(self.__Table[i]['answer']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 1, item)

        return model

