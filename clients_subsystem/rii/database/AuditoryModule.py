from dbConnector import DataBaseModule as DBM

class Auditory(object):
    def __init__(self):
        super().__init__()

    def getList(self):
        sql = "SELECT * FROM audtable"
        data = DBM.GetData(sql=sql, nameDB='riidb')
        return data