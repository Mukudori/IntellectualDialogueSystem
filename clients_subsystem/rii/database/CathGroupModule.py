from dbConnector import DataBaseModule as DBM

class CathGroup(object):
    def __init__(self):
        super().__init__()

    def getList(self, idCath=0):
        if idCath:
            sql = "SELECT cathGroup.id as id, cathGroup.name as name, " \
                  "cathGroup.course as course, clients.fio as fioCur, " \
                  "cathedra.name as nameCathedra " \
                  "FROM (riidb.cathGroup INNER JOIN riidb.clients " \
                  "ON cathGroup.idCurator = clients.id) INNER JOIN " \
                  "riidb.cathedra ON cathGroup.idCathedra = cathedra.id " \
                  "AND cathedra.id='%s';" % idCath
        else:
            sql = "SELECT * FROM cathGroup"
        data = DBM.GetData(sql=sql, nameDB='riidb')

        return data

    def getTVCathGroup(self, idCathedra=0):
        if not idCathedra:
            sql = "SELECT cathGroup.id as idGroup, cathGroup.name as nameGroup, " \
                  "cathGroup.course as course, clients.fio as fioCur, cathedra.name as nameCathedra " \
                  "FROM (riidb.cathGroup INNER JOIN riidb.clients " \
                  "ON cathGroup.idCurator = clients.id) INNER JOIN riidb.cathedra " \
                  "ON cathGroup.idCathedra = cathedra.id;"
        else:
            sql = "SELECT cathGroup.id as idGroup, cathGroup.name as nameGroup, " \
                  "cathGroup.course as course, clients.fio as fioCur, cathedra.name as nameCathedra " \
                  "FROM (riidb.cathGroup INNER JOIN riidb.clients " \
                  "ON cathGroup.idCurator = clients.id) INNER JOIN riidb.cathedra " \
                  "ON cathGroup.idCathedra = cathedra.id AND cathedra.id='%s';"%idCathedra
        fieldTab = ['idGroup', 'nameGroup', 'course', 'fioCur', 'nameCathedra']
        fieldView = ['id', 'Группа','Курс', "Куратор", "Кафедра"]
        model=DBM.CreateTableViewModel(sql,fieldTab,fieldView, 'riidb')
        return model

    def getFromID(self, id):
        sql = "SELECT id, name, idCathedra, idCurator, course " \
              "FROM riidb.cathGroup " \
              "WHERE id ='%s';"%id
        record = DBM.GetData(sql=sql, nameDB='riidb')[0]
        return record

    def insertRecord(self, name, idCath, idTeacher, course):
        sql = "INSERT INTO riidb.cathGroup " \
              "(name, idCathedra, idCurator, course) " \
              "VALUES ('%s', '%s', '%s', '%s')" % (name,idCath,idTeacher, course)
        idCathGroup = DBM.ExecuteSQL(sql=sql, nameDB='riidb')
        return idCathGroup

    def updateRecord(self, id, name, idCath, idTeacher, course):
        sql = "UPDATE riidb.cathGroup " \
              "SET name='%s', idCathedra='%s', idCurator='%s', course='%s' " \
              "WHERE id='%s';"%(name,idCath,idTeacher,course,id)
        DBM.ExecuteSQL(sql=sql, nameDB='riidb')
