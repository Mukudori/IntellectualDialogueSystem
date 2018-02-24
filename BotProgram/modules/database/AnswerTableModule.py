from modules.database import DataBaseModule
from modules.database.ActionTableModule import ActionTable
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore

class AnswerTable:

    def __init__(self):
        self.init = True



    def GetAllData(self):
        return self.__Table

    def __RefreshTable(self):
        self.__Table = DataBaseModule.GetData('SELECT * FROM answertab')


    def GetDataFromID(self,id):
        pass
    def GetAnswerFromID(self,id):
        self.__RefreshTable()
        for record in self.__Table:
            if record['id']==id: return record['answer']
        return 0

    def GetTableViewModel(self):
        return DataBaseModule.CreateTableViewModel('SELECT * FROM answertab',
                                                   ['id', 'answer', 'idAction'],
                                                   ['id', 'Ответ', 'Действие'])

    def InsertRecord(self,answer,idContext):
        currentid = DataBaseModule.ExecuteSQL(
                "INSERT INTO answertab (answer, idContext) "+
                "VALUES('" + answer +"','"+str(idContext)+"');" )
        return currentid

    def UpdateRecord(self,id,answer):
        pass

    def DeleteFromID(self, id):
        DataBaseModule.ExecuteSQL(
            """DELETE FROM answertab
                WHERE answertab.id = '"""+str(id)+"';"
        )

    def UpdateRecord(self, id, answer, idAction):
        DataBaseModule.ExecuteSQL(
            "UPDATE answertab "+
            "SET answer ='"+answer+"', idAction ='"+str(idAction)+"' "+
            "WHERE id='"+str(id)+"';"
        )

    def DeleteFromContextID(self, idContext):
        DataBaseModule.ExecuteSQL(
            """DELETE FROM answertab 
            WHERE idContext = '"""+str(idContext)+"';"
        )

    def GetAnswerAndActionFromAnswerID(self, id):
        data = DataBaseModule.GetData(
            """
            SELECT answertab.answer as 'ans', actiontab.action as 'act' 
            FROM botdb.answertab INNER JOIN botdb.actiontab ON answertab.idAction = actiontab.id 
            WHERE answertab.id = '""" + str(id)+"';"
        )

        return (data[0]['ans'], data[0]['act'])