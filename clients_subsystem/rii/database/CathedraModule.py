from dbConnector import DataBaseModule as DBM

class Cathedra(object):
    def __init__(self):
        super().__init__()

    def getTVCathedraModel(self, zav=True):

        if zav:
            sql = "SELECT cathedra.id as id, cathedra.name as name," \
              " clients.fio as zav " \
              "FROM riidb.cathedra INNER JOIN riidb.clients " \
              "ON cathedra.idZav = clients.id;"
            nameList = ['id', 'name', 'zav']
            asList = ['id', "Кафедра", "Заведующий"]
        else:
            sql = "SELECT * FROM riidb.cathedra"
            nameList = ['id', 'name', 'idZav']
            asList = ['id', "Кафедра", "Заведующий"]

        model = DBM.CreateTableViewModel(sql, nameList, asList, nameDB='riidb')
        return model

    def getData(self):
        sql = "SELECT * FROM riidb.cathedra"
        data = DBM.GetData(sql=sql, nameDB='riidb')
        return data

    def getList(self):
        SQL = "SELECT * " \
              "FROM riidb.cathedra;"
        data = DBM.GetData(sql=SQL, nameDB='riidb')
        return data

    def getRecord(self, id):
        sql = "SELECT id, name, idZav " \
              "FROM riidb.cathedra " \
              "WHERE id ='%s';" % id
        data = DBM.GetData(sql=sql, nameDB='riidb')[0]
        return data

    def insertRecord(self, name, idZav):
        sql = "INSERT INTO riidb.cathedra " \
              "(name, idZav) " \
              "VALUES ('%s', '%s');" % (name,idZav)
        idRec = DBM.ExecuteSQL(sql=sql, nameDB='riidb')
        return idRec

    def updateRecord(self, id, name, idZav):
        sql = "UPDATE riidb.cathedra " \
              "SET name='%s', idZav='%s' " \
              "WHERE id='%s';" % (name, idZav,id)
        DBM.ExecuteSQL(sql=sql, nameDB='riidb')