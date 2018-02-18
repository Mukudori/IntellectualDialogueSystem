from modules.database import DataBaseModule
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore
from modules.database import DataBaseModule

class ContextTable:
    """Таблица контекста диалога. Связывает все, что связано с диалогами.
    Вопросы и ответы неотделимы от контекста"""
    def __init__(self):
        self.__RefreshShortTable()
        self.CurrentRecord = 0

    def __RefreshShortTable(self):
        self.__Table = DataBaseModule.GetData('SELECT * FROM contexttab')
        self.__shortTable = True

    def __RefreshLongTable(self):
        pass

    def GetTableViewModel(self):
        model = QStandardItemModel()
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
            model.setItem(i, 3, item)
        return model

    def GetStrFromID(self, id):
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




