import DataBaseModule

class ActionTable:

    def __init__(self):
        self.__Table = DataBaseModule.GetData('SELECT * FROM actiontab')

    def GetAllData(self):
        return self.__Table

    def GetActionFromID(self, id):
        for record in self.__Table:
            if record['id'] == id:
                return record['action']
        return 0