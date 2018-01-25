from database import DataBaseModule
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore


class ActionTable:

    def __init__(self):
        self.__RefreshTable()

    def GetAllData(self):
        return self.__Table

    def __RefreshTable(self):
        self.__Table = DataBaseModule.GetData('SELECT * FROM actiontab')

    def GetActionFromID(self, id):
        for record in self.__Table:
            if record['id'] == id:
                return record['action']
        return 0

    def GetList(self):
        itemList = list()
        for record in self.__Table:
            itemList.append(record['action'])
        return itemList

    def GetTableViewModel(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['id','Название действия','Комманды', 'Доп.Инфо'])
        model.setVerticalHeaderLabels([' ']*len(self.__Table))

        for i in range(len(self.__Table)):
            item = QStandardItem(str(self.__Table[i]['id']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 0, item)

            item = QStandardItem(str(self.__Table[i]['action']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 1, item)

            item = QStandardItem(str(self.__Table[i]['command']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 2, item)

            item = QStandardItem(str(self.__Table[i]['note']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 3, item)

        return model

    def InsertRecord(self, action, comands, note):
        currentid = DataBaseModule.ExecuteSQL('''
            INSERT INTO actiontab (action,command,note) 
            VALUES (\'''' + action+"','"+comands+"','"+note+"');")
        return currentid

    def UpdateRecord(self,id,action, comands, note):
        DataBaseModule.ExecuteSQL('''
        UPDATE actiontab 
        SET action=\''''+action+"', command='"+comands+"', note='"+note+"'"
       +"WHERE id='"+str(id)+"';")

    def DeleteRecord(self, id):
        DataBaseModule.ExecuteSQL(
        "DELETE FROM actiontab WHERE id ='"+str(id)+"';")

    def GetDataFromID(self, id):
        for rec in self.__Table:
            if rec['id'] == id:
                return rec
        return 0

    def GetIDFromActionStr(self, action):
        for rec in self.__Table:
            if rec['action'].upper() == action.upper():
                return rec['id']
        return 0




