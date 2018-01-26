from database import DataBaseModule
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore
import StringFunctionsModule


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


    def FindQuestionID(self, message):
        coef = 0
        id = 0
        wList = StringFunctionsModule.GetWordsListFromText(message)
        for rec in self.__Table:
            precoef = 0
            question = rec['question'].upper()
            for word in wList:
                if word in question:
                    precoef += 1
            if (precoef):
                precoef = len(StringFunctionsModule.GetWordsListFromText(question)) / precoef
                if (precoef > coef):
                    coef = precoef
                    id = rec['id']

        return id


