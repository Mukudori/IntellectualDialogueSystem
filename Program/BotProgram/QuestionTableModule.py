import DataBaseModule

class QuestionTable:

    def __init__(self):
        self.__Table = DataBaseModule.GetData('SELECT * FROM questiontab')

    def GetAllData(self):
        return  self.__Table

    def GetDataFromID(self, id):
        pass

    def GetQuestionFromID(self, id):
        for record in self.__Table:
            if record['id']==id:
                return record['question']
        return 0