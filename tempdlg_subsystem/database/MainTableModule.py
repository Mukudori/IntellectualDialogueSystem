from dbConnector import DataBaseModule

"""Хотел содать базовый класс для таблиц,
но решил, что прорще каждой таблице создавать класс индивидуально,
а не перегружать базовые методы"""

class MainOneTable:
    def __init__(self, tableName, fieldList):
        self.tableList = tableName
        self.fieldList = fieldList

    def __RefreshTable(self):
        sql='SELECT '
        for table in self.tableList:
            for field in self.fieldList:
                sql+=table+'.'+field+', '
        sql = sql[:-2] + ' FROM '



        self.__Table = DataBaseModule.GetData('SELECT * FROM actiontab')

