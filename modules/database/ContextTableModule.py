# -*- coding: utf-8 -*-
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore
from modules.database import DataBaseModule
from modules.database.AnswerTableModule import AnswerTable
from modules.database.QuestionTableModule import QuestionTable
from modules.database.AccessTableModule import AccessTable

class ContextTable:
    """Таблица контекста диалога. Связывает все, что связано с диалогами.
    Вопросы и ответы неотделимы от контекста"""
    def __init__(self):
        self.__Table = 0
        self.CurrentRecord = 0

    def __RefreshTable(self):
        self.__Table = DataBaseModule.GetData('SELECT * FROM contexttab')



    def GetTableViewModel(self):
        """model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['id','Заголовок контекста', 'id Родителя', 'Группы пользователей'])
        model.setVerticalHeaderLabels([' ']*len(self.__Table))

        for i in range(len(self.__Table)):
            item = QStandardItem(str(self.__Table[i]['id']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 0, item)

            item = QStandardItem(str(self.__Table[i]['header']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 1, item)

            item = QStandardItem(str(self.__Table[i]['idParent']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 2, item)

            item = QStandardItem(str(self.__Table[i]['idGroupStr']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 3, item)"""
        sql = 'SELECT * FROM contexttab'

        model = DataBaseModule.CreateTableViewModel(sql, ['id', 'header', 'idParent', 'level'], ['id', 'Заголовок контекста', 'id Родителя', 'Уровень'])
        return model

    def GetStrFromID(self, id):
        self.__RefreshTable()
        for rec in self.__Table:
            if rec['id'] == id:
                return rec['header']
        return str()

    def __QuestionOrAnswerModel(self, idCon, tabAnswer=False):

        tabNam = str()
        tabField = str()
        header = str()
        dlgField = str()
        if tabAnswer:
            tabNam = 'answertab'
            tabField = 'answer'
            header = 'Ответ'
            dlgField='idA'
        else:
            tabNam = 'questiontab'
            tabField = 'question'
            header = 'Вопрос'
            dlgField = 'idQ'

        sql = "SELECT botdb."+tabNam+".id, "+tabNam+"."+tabField +"""
        FROM botdb.contexttab INNER JOIN botdb."""+tabNam+""" 
        ON contexttab.id = """+tabNam+""".idContext  
        WHERE contexttab.id = '"""+str(idCon)+"';"

        data = DataBaseModule.GetData(sql)
        model = QStandardItemModel()

        if tabAnswer:
            header = ['id', header, 'Действие']
            sql = """SELECT actiontab.action
            FROM botdb.actiontab INNER JOIN (botdb.contexttab INNER JOIN botdb.answertab  
            ON contexttab.id = answertab.idContext) ON actiontab.id = answertab.idAction
            WHERE contexttab.id = '"""+ str(idCon)+"';"
            colAction = DataBaseModule.GetData(sql)

        else:
            header = ['id', header]

        model.setHorizontalHeaderLabels(header)
        model.setVerticalHeaderLabels([' '] * len(data))


        for i in range(len(data)):
            item = QStandardItem(str(data[i]['id']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 0, item)

            item = QStandardItem(str(data[i][tabField]))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 1, item)
            if tabAnswer:
                item = QStandardItem(colAction[i]['action'])
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                model.setItem(i, 2, item)
        return model

    def GetQuestionsModelFromContextID(self, id):
        return self.__QuestionOrAnswerModel(id,False)

    def GetAnswerModelFromContextID(self,id):
        return self.__QuestionOrAnswerModel(id, True)

    def GetRecordFromID(self,id):
        self.__RefreshTable()
        for rec in self.__Table:
            if rec['id']==id:
                self.CurrentRecord = rec
                return rec
        self.CurrentRecord = {'id' : 0, 'header' : str(), 'idParent' : 0, 'idGroupStr' : str()}
        return self.CurrentRecord

    def GetChildContextModelFromParentID(self, id):
        sql = """SELECT contexttab.id, contexttab.header 
        FROM botdb.contexttab 
        WHERE contexttab.idParent='"""+str(id)+"';"
        data = DataBaseModule.GetData(sql)
        model = QStandardItemModel()
        if len(data):
            model.setHorizontalHeaderLabels(['id', 'Заголовок контекста'])
            model.setVerticalHeaderLabels([' '] * len(data))

            for i in range(len(data)):
                item = QStandardItem(str(data[i]['id']))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                model.setItem(i, 0, item)

                item = QStandardItem(str(data[i]['header']))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                model.setItem(i, 1, item)
        else:
            model.setHorizontalHeaderLabels(['Отсутствуют'])

        return model

    def GetGroupsModelFromID(self, id):
        sql = """SELECT usergrouptab.id as 'id', usergrouptab.nameGroup as 'nameGroup'
        FROM botdb.usergrouptab INNER JOIN (botdb.accesstab
        INNER JOIN botdb.contexttab ON accesstab.idContext = contexttab.id)
        ON usergrouptab.id = accesstab.idGroup 
        WHERE contexttab.id='"""+str(id)+"';"
        model = DataBaseModule.CreateTableViewModel(sql, ['id', 'nameGroup'], ['id', 'Группа'])
        return model

    def InsertRecord(self, header, idParent, level):
       id = DataBaseModule.ExecuteSQL("""
        INSERT INTO contexttab (header, idParent, level) 
        VALUES ('""" +header+"','"+str(idParent)+"','"+str(level)+"');")
       return id

    def _DeleteRecordFromID(self, idContext):
        QuestionTable().DeleteFromContextID(idContext)
        AnswerTable().DeleteFromContextID(idContext)
        AccessTable().DeleteFromContextID(idContext)
        DataBaseModule.ExecuteSQL(
            """DELETE FROM contexttab 
            WHERE id = '"""+str(idContext)+"';"
        )

    def CascadeDeleteFromID(self, idContext):
        idConList = [idContext]
        self.__RefreshTable()

        for rec in self.__Table:
            idP = idConList[-1]
            if idP and rec['idParent'] == idP:
                idConList.append(rec['id'])

        idConList = idConList[-1::-1]

        for idCon in idConList:
            self._DeleteRecordFromID(idCon)

    def UpdateRecord(self, id, header):
        DataBaseModule.ExecuteSQL(
            """UPDATE contexttab 
            SET header='"""+header+"""' 
            WHERE id ='"""+str(id)+"';"
        )

    def GetIDDictFromLevel(self, level, idGroup):
        data = DataBaseModule.GetData("""SELECT id, level, idParent FROM contexttab 
        WHERE level = '"""+str(level)+"';")


        retData =  ({'id' : 0, 'level': 0, 'idParent' : 0}, )
        for rec in data:
            if {'idGroup': idGroup} in  self.GetGroupDict(rec['id']):
                retData+=(rec,)


        return retData

    def GetGroupDict(self, idContext):
        data = DataBaseModule.GetData(
            """
            SELECT usergrouptab.id as 'idGroup' FROM botdb.usergrouptab INNER JOIN 
            (botdb.contexttab INNER JOIN botdb.accesstab ON contexttab.id = accesstab.idContext )
            ON usergrouptab.id = accesstab.idGroup 
            WHERE contexttab.id = '"""+str(idContext)+"';"
        )

        return self.ConvertData(data)

    def GetQuestionDictFromContextID(self,idContext, idGroup):
        groupDict = self.GetGroupDict(idContext)

        if {'idGroup': idGroup} in groupDict:
            data = DataBaseModule.GetData(
                """
                SELECT questiontab.id as 'idQ', questiontab.question as 'question', 
                contexttab.id as 'idC', contexttab.level as 'level', contexttab.idParent as 'idParent' 
                FROM botdb.questiontab INNER JOIN botdb.contexttab 
                ON questiontab.idContext = contexttab.id 
                WHERE contexttab.id='"""+str(idContext)+"';"
            )
            return self.ConvertData(data)

    def GetChildContextIDList(self, idContext,idGroup):
        groupDict = self.GetGroupDict(idContext)

        if {'idGroup': idGroup} in groupDict:
            data = DataBaseModule.GetData(
                """
                SELECT id, level, idParent FROM botdb.contexttab 
                WHERE idParent = '"""+str(idContext)+"';"
            )
            return self.ConvertData(data)

    def GetRecordFromID(self, idContext):
        data = DataBaseModule.GetData(
            """
            SELECT id, level, idParent FROM botdb.contexttab 
            WHERE id = '""" + str(idContext) + "';"
        )
        return self.ConvertData(data)

    def GetIDParent(self, idContext, idGroup):
        child = self.GetRecordFromID(idContext)
        groupDict = self.GetGroupDict(child[0]['idParent'])
        data =0
        if {'idGroup': idGroup} in groupDict:
            data = self.GetRecordFromID(child[0]['idParent'])
        if data:
            return self.ConvertData(data)
        else:
            return self.ConvertData({'id' : 0, 'level' : 0, 'idParent' : 0})

    def GetParentParentChildContextIDList(self, idContext, idGroup):
        parentid = self.GetIDParent(idContext, idGroup)
        parentid = self.GetIDParent(parentid[0]['id'], idGroup)
        groupDict = self.GetGroupDict(parentid[0]['id'])
        if {'idGroup': idGroup} in groupDict:
            if parentid[0]['level']:
                return self.GetChildContextIDList(parentid[0]['id'], idGroup)
            else:
                return self.GetIDDictFromLevel(0,idGroup)

    def ConvertData(self, data):
        if type(data) == type(tuple()):
            return data
        else:
            return (data,)



