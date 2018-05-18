from dbConnector import DataBaseModule as DBM

class Auditory(object):
    def __init__(self):
        super().__init__()

    def getList(self):
        sql = "SELECT id, num FROM riidb.audtable " \
              "ORDER BY num"
        data = DBM.GetData(sql=sql, nameDB='riidb')
        return data

    def insertRecord(self, numAuditory):
        sql = "INSERT INTO riidb.audtable (num) " \
              "VALUES ('%s')" % numAuditory
        insertIndex = DBM.ExecuteSQL(sql=sql, nameDB='riidb')
        return insertIndex

    def getTVModel(self):
        sql = "SELECT id, num FROM riidb.audtable " \
              "ORDER BY num"
        fieldsTable = ['id', 'num']
        fieldsView = ['id', 'Номер аудитории']
        model = DBM.CreateTableViewModel(sql=sql,fieldTab=fieldsTable,
                                         fieldsView=fieldsView, nameDB='riidb')
        return model

    def deleteRecord(self, id):
        sql = "DELETE FROM riidb.audtable " \
              "WHERE id = '%s' " % id
        DBM.ExecuteSQL(sql=sql, nameDB='riidb')