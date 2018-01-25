from database import DataBaseModule
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore



class QuestionTable:

    def __init__(self):
        self.__Connect()

    def __Connect(self):
        self.__Table = DataBaseModule.GetData('SELECT * FROM questiontab')

    def GetAllData(self):
        return  self.__Table

    def GetDataFromID(self, id):
        pass

    def GetQuestionFromID(self, id):
        for record in self.__Table:
            if record['id']==id:
                return record['question']
        return 0

    def GetTableViewModel(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['id', 'Вопрос'])
        model.setVerticalHeaderLabels([' '] * len(self.__Table))

        for i in range(len(self.__Table)):
            item = QStandardItem(str(self.__Table[i]['id']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 0, item)

            item = QStandardItem(str(self.__Table[i]['question']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 1, item)

        return model


    def InsertRecord(self, question):
        currentid = DataBaseModule.ExecuteSQL('''
        INSERT INTO questiontab (question)
         VALUES("''' +question+'");' )
        return  currentid

    def UpdateRecordFromIDAndText(self, id, question):
        DataBaseModule.ExecuteSQL(
            "UPDATE questiontab "+
            "SET question ='"+question+"' "+
            "WHERE id='"+str(id)+"';"
        )