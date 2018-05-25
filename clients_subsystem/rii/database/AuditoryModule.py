from dbConnector import DataBaseModule as DBM
from clients_subsystem.rii.database.TimeTableModule import TimeTable

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

    def getAuditoryInfo(self, numAud, numDay, numLesson):
        audList = self.getList()
        info = None
        for row in audList:
            if row['num'] == numAud:
                info = row

        if info:
            info['checkLesson'] = False
            dop_inf= TimeTable().getAudInfo(id=info['id'],
                                            numDay=numDay,
                                            numLesson=numLesson
                                            )
            if dop_inf:
                info['checkLesson'] = True
                info = {**info, **dop_inf}
            return info
