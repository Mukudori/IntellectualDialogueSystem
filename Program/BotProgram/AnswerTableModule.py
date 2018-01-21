import DataBaseModule

class AnswerTable:

    def __init__(self):
        self.__Table = DataBaseModule.GetData('SELECT * FROM answertab')

    def GetAllData(self):
        return self.__Table

    def GetDataFromID(self,id):
        pass
    def GetAnswerFromID(self,id):
        for record in self.__Table:
            if record['id']==id: return record['answer']
        return 0
