# -*- coding: utf-8 -*-
from dbConnector import DataBaseModule
import tempdlg_subsystem.StringFunctionsModule


class QuestionTable:

   # def __init__(self):
        #self.__Connect()
       # super(QuestionTable, self).__init__()

    def __Connect(self):
        self.__Table = DataBaseModule.GetData('SELECT * FROM questiontab')

    def GetAllData(self):
        return  self.__Table

    def GetDataFromID(self, id):
        pass

    def GetQuestionFromID(self, id):
        """
        for record in self.__Table:
            if record['id']==id:
                return record['question']
                """
        data = DataBaseModule.GetData(
            """
            SELECT question FROM botdb.questiontab 
            WHERE id ='"""+str(id)+"';"
        )
        return data[0]['question']

    def GetTableViewModel(self):
        """model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['id', 'Вопрос'])
        model.setVerticalHeaderLabels([' '] * len(self.__Table))

        for i in range(len(self.__Table)):
            item = QStandardItem(str(self.__Table[i]['id']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 0, item)

            item = QStandardItem(str(self.__Table[i]['question']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 1, item)"""

        return DataBaseModule.CreateTableViewModel(
            'SELECT * FROM questiontab',
            ['id','question'],
            ['id', 'Вопрос']
        )


    def InsertRecord(self, question, idContext):
        currentid = DataBaseModule.ExecuteSQL("""
        INSERT INTO questiontab (question, idContext)
         VALUES('""" + question +"','" + str(idContext) +"');")
        return  currentid

    def UpdateRecordFromIDAndText(self, id, question):
        DataBaseModule.ExecuteSQL(
            "UPDATE questiontab "+
            "SET question ='"+question+"' "+
            "WHERE id='"+str(id)+"';"
        )

    def DeleteFromID(self, id):
        DataBaseModule.ExecuteSQL(
            """DELETE FROM questiontab
                WHERE questiontab.id = '""" + str(id) + "';"
        )

    def GetModelFromContextID(self, id):
        pass


    def FindQuestionID(self, message):
        coef = 0
        id = 0
        wList = tempdlg_subsystem.StringFunctionsModule.GetWordsListFromText(message)
        for rec in self.__Table:
            precoef = 0
            question = rec['question'].upper()
            for word in wList:
                if word in question:
                    precoef += 1
            if (precoef):
               # precoef = precoef/len(StringFunctionsModule.GetWordsListFromText(question))
                if (precoef > coef):
                    coef = precoef
                    id = rec['id']

        return id

    def DeleteFromContextID(self, idContext):
        DataBaseModule.ExecuteSQL(
            """DELETE FROM questiontab 
            WHERE idContext = '"""+str(idContext)+"';"
        )


