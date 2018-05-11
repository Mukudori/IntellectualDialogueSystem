from dbConnector import DataBaseModule as DBM

class Cathedra(object):
    def __init__(self):
        super().__init__()

    def getTVCathedraModel(self):
        sql = "SELECT cathedra.id as id, cathedra.name as name," \
              " clients.fio as zav " \
              "FROM riidb.cathedra INNER JOIN riidb.clients " \
              "ON cathedra.idZav = clients.id;"
        nameList = ['id', 'name', 'zav']
        asList = ['id', "Кафедра", "Заведующий"]
        model = DBM.CreateTableViewModel(sql, nameList, asList, nameDB='riidb')
        return model

    def getData(self):
        sql = "SELECT * FROM riidb.cathedra"
        data = DBM.GetData(sql=sql, nameDB='riidb')
        return data