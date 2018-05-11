# -*- coding: utf-8 -*-
from dbConnector import DataBaseModule
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore


class ActionTable:

    def __init__(self):

        self.__Table = 0

    def GetAllData(self):
        return self.__Table

    def __RefreshTable(self):
        self.__Table = DataBaseModule.GetData('SELECT * FROM actiontab')

    def GetActionFromID(self, id):
        self.__RefreshTable()
        for record in self.__Table:
            if record['id'] == id:
                return record['action']
        return str()

    def GetList(self):
        self.__RefreshTable()
        itemList = list()
        for record in self.__Table:
            itemList.append(record['action'])
        return itemList

    def GetTableViewModel(self):
        self.__RefreshTable()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['id','Название действия', 'Доп.Инфо'])
        model.setVerticalHeaderLabels([' ']*len(self.__Table))

        for i in range(len(self.__Table)):
            item = QStandardItem(str(self.__Table[i]['id']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 0, item)

            item = QStandardItem(str(self.__Table[i]['action']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 1, item)

            item = QStandardItem(str(self.__Table[i]['note']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 2, item)

        return model

    def InsertRecord(self, action, note, scrypt = 0):
        if scrypt:
            check =1
        else:
            check = 0

        currentid = DataBaseModule.ExecuteSQL('''
            INSERT INTO actiontab (action,note,scrypt) 
            VALUES (\'''' + action +"','" + note +"','" + str(check) +"');")

        return currentid

    def UpdateRecord(self,id,action, note, scrypt =0):
        if scrypt:
            check =1
        else:
            check = 0

        DataBaseModule.ExecuteSQL('''
        UPDATE actiontab 
        SET action=\'''' + action +"', note='" + note +"', scrypt ='" + str(check) +"' " +
        "WHERE id='" + str(id) +"';")


    def DeleteRecord(self, id):
        DataBaseModule.ExecuteSQL(
        "DELETE FROM actiontab WHERE id ='"+str(id)+"';")

    def GetDataFromID(self, id):
        self.__RefreshTable()
        for rec in self.__Table:
            if rec['id'] == id:
                return rec
        return 0

    def GetIDFromActionStr(self, action):
        self.__RefreshTable()
        for rec in self.__Table:
            if rec['action'].upper() == action.upper():
                return rec['id']
        return 0

    def GetStringAndIDList(self):
        self.__RefreshTable()
        return [[rec['id'], rec['action']] for rec in self.__Table]

    def CheckScryptFromIDAction(self, idAction):
        data = DataBaseModule.GetData(
            """
            SELECT scrypt FROM botdb.actiontab 
            WHERE id = '"""+str(idAction)+"';"
        )
        return data[0]['scrypt']





