from dbConnector import DataBaseModule as DBM
from clients_subsystem.rii.database.AuditoryModule import Auditory
from clients_subsystem.rii.database.ClientModule import Client

class Projectors(object):
    def __init__(self):
        super().__init__()

    def getList(self):
        sql = "SELECT * from riidb.projectors"
        data = DBM.GetData(sql = sql, nameDB="riidb")
        return data

    def insertRecord(self):
        pass

    def deleteRecord(self):
        pass

    def getTVModel(self):
        sql = "SELECT * from riidb.projectors"
        fieldsTab = ['id', 'name', 'numAud']
        fieldsView = ['id', 'Название', "Ауд."]
        model = DBM.CreateTableViewModel(sql=sql, fieldsView=fieldsView,
                                         fieldTab=fieldsTab,
                                         nameDB='riidb')
        return model

    def updateRecord(self, id, name=0, numAud=0, idClient=0):
        sql = "UPDATE riidb.projectors SET "

        if name and idAud:
            sql += "name = '%s', idAud = '%s' " % (name, numAud)
        elif name:
            sql += "name = '%s' " % name
        else:
            sql += "numAud = '%s', idClient='%s'" % (numAud,idClient)

        sql+= "WHERE id = '%s';" % id
        DBM.ExecuteSQL(sql=sql, nameDB='riidb')

    def reserveDevice(self, nameDevice, numAud, idClient):
        data = self.getList()
        device = 0
        for row in data:
            if row['name'].upper() == nameDevice.upper():
                device = row
                break

        if device:
            if device['numAud']!='0':
                cl = Client().getFromID(id = device['idClient'])
                return {'error' : 1,
                        'text' : 'Устройство уже занято: %s ауд. - %s'
                                  % (device['numAud'],cl['shortfio'])}
            else:
                self.updateRecord(id=device['id'],
                                  numAud=numAud,
                                  idClient = idClient)
                return {'error': 0, 'text': "За вами зарезервировано "
                                            "устройство %s в аудитории %s "
                                            % (device['name'], numAud)}
        else:
            return {'error' : 1, 'text' : 'Неправильное имя устройства'}


    def getListInfo(self):
        data = self.getList()

        for row in data:
            if row['numAud']=="0":
                row['numAud'] = "На кафедре"
            if row['idClient']:
                client = Client().getFromID(row['idClient'])
                if client:
                    row['fioClient'] = client['shortfio']
                else:
                    row['fioClient'] = "-"
            else:
                row['fioClient'] = "-"

        return data

    def returnToCath(self, idClient):
        data = self.getList()
        device=0
        for row in data:
            if row['idClient'] == idClient:
                device = row['name']

        sql = "UPDATE riidb.projectors " \
              "SET numAud = 0, idClient =0 " \
              "WHERE idClient = '%s'" % idClient
        DBM.ExecuteSQL(sql=sql, nameDB='riidb')

        return device
