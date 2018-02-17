from modules.database import DataBaseModule
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore

class UserGroup:
    def __init__(self):
        self.__refreshTable()

    def __refreshTable(self):
        self.__Table = DataBaseModule.GetData('SELECT * FROM usergrouptab')

    def InsertRecord(self, **rec):
        currentid = DataBaseModule.ExecuteSQL('''
                   INSERT INTO usergrouptab (nameGroup, editDB) 
                   VALUES (\'''' +rec['nameGroup'] + "', '"+str(rec['editDB'])+"');")
        return currentid

    def DeleteRecord(self, id):
        DataBaseModule.ExecuteSQL(
            "DELETE FROM usergrouptab WHERE id ='" + str(id) + "';")

    def GetDataFromID(self, id):
        for rec in self.__Table:
            if rec['id'] == id:
                return rec
        return 0

    def GetTableViewModel(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['id','Название группы','Редактирование БД'])
        model.setVerticalHeaderLabels([' ']*len(self.__Table))

        for i in range(len(self.__Table)):
            item = QStandardItem(str(self.__Table[i]['id']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 0, item)

            item = QStandardItem(str(self.__Table[i]['nameGroup']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 1, item)

            item = QStandardItem(str(self.__Table[i]['editDB']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 2, item)

        return model

    def UpdateRecord(self, **rec):
        DataBaseModule.ExecuteSQL('''
                UPDATE usergrouptab 
                SET nameGroup=\'''' + rec['nameGroup'] + "', editDB='"+str(rec['editDB'])+ "'"
                                  + "WHERE id='" + str(rec['id']) + "';")









