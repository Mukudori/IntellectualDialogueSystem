from dbConnector import DataBaseModule as DBM

class CathGroup(object):
    def __init__(self):
        super().__init__()

    def getList(self):
        sql = "SELECT * FROM cathGroup"
        data = DBM.GetData(sql=sql, nameDB='riidb')
        return data

    def getTVCathGroup(self):
        sql = "SELECT cathGroup.id as idGroup, cathGroup.name as nameGroup, " \
              "clients.fio as fioCur, cathedra.name as nameCathedra " \
              "FROM (riidb.cathGroup INNER JOIN riidb.clients " \
              "ON cathGroup.idCurator = clients.id) INNER JOIN riidb.cathedra " \
              "ON cathGroup.idCathedra = cathedra.id;"
        fieldTab = ['idGroup', 'nameGroup', 'fioCur', 'nameCathedra']
        fieldView = ['id', 'Группа', "Куратор", "Кафедра"]
        model=DBM.CreateTableViewModel(sql,fieldTab,fieldView, 'riidb')
        return model
