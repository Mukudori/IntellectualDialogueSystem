from dbConnector import DataBaseModule as DMB

class Prohectors(object):
    def __init__(self):
        super().__init__()

    def getList(self):
        sql = "SELECT * from riidb.projectors"
        data = DMB.GetData(sql = sql, nameDB="riidb")
        return data

    def insertRecord(self):
        pass

    def deleteRecord(self):
        pass

    def getTVModel(self):
        sql = "SELECT * from riidb.projectors"
        fieldsTab = ['id', 'name', 'numAud']
        fieldsView = ['id', 'Название', "Ауд."]
        model = DMB.CreateTableViewModel(sql=sql, fieldsView=fieldsView,
                                         fieldTab=fieldsTab,
                                         nameDB='riidb')
        return model