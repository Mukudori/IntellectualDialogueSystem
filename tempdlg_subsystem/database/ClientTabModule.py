from dbConnector import DataBaseModule as DBM
from clients_subsystem.rii.database.ClientModule import Client
from clients_subsystem.rii.database.CathGroupModule import CathGroup

class ClientsTab(object):
    def __init__(self):
        super().__init__()

    def getAllData(self):
        sql = "SELECT * FROM botdb.clientstab"
        data = DBM.GetData(sql=sql, nameDB='botdb')
        return data

    def getRecordFromID(self, id):
        sql = "SELECT id, idRii, idTelegram, idClientGroup " \
              "FROM botdb.clientstab " \
              "WHERE id = '%s';" % id
        data = DBM.GetData(sql=sql, nameDB='botdb')[0]
        if "Error" in data.keys():
            return 0
        else: data

    def getRecordFromIDTelegram(self, idTelegram):
        sql = "SELECT id, idRii, idTelegram, idClientGroup " \
              "FROM botdb.clientstab " \
              "WHERE idTelegram = '%s';" % idTelegram
        data = DBM.GetData(sql=sql, nameDB='botdb')
        #data = data[0]
        if len(data)==0 or "Error" in data[0].keys():
            return 0
        else:
            data = data[0]
            idClient = data['idRii']
            idGroup = data['idClientGroup']
            data2=0
            if idGroup==2:
                data2 = Client().getFromID(id=idClient)
            elif idGroup == 3:
                data2 = CathGroup().getFromID(id=idClient)
            if data2:
                return {**data, **data2}
            else:
                return data

    def getRecordFromIDRII(self, idRii, idUserGroup):
        sql = "SELECT id, idRii, idTelegram, idClientGroup " \
              "FROM botdb.clientstab " \
              "WHERE idRii = '%s' AND idClientGroup = '%s';" % (idRii,idUserGroup)
        data = DBM.GetData(sql=sql, nameDB='botdb')
        # data = data[0]
        if len(data) == 0 or "Error" in data[0].keys():
            return 0
        else:
            return data[0]


    def _getFromRIIDB(self, idRii):
        record = Client().getFromID(id=idRii)
        return record


    def getInfoFromIDTelegram(self, idTelegram):
        rec = self.getRecordFromIDTelegram(idTelegram=idTelegram)
        if rec:

            try:
                r = self._getFromRIIDB(idRii=rec['idClient'])
                if type(r) == type(dict()):
                    del r['id']
                    rec = {**rec, **r}
                    rec['idClient'] = rec['id']
            except KeyError:
                pass
        return rec

    def getTVModel(self):
        sql = "SELECT * FROM botdb.clientstab"
        fieldsTable = ['id', 'idRii', 'idClientGroup', 'idTelegram']
        model = DBM.CreateTableViewModel(sql=sql, fieldsView=fieldsTable,
                                         fieldTab=fieldsTable, nameDB='botdb')
        return model

    def insertClient(self, idClient, idClientGroup, idTelegram):
        sql = "INSERT INTO botdb.clientstab (idRii, idClientGroup, idTelegram) " \
              "VALUES ('%s', '%s','%s')" % (idClient, idClientGroup, idTelegram)
        insertID = DBM.ExecuteSQL(sql=sql, nameDB='botdb')
        return insertID

    def deleteClient(self, idTelegram):
        sql = "DELETE FROM botdb.clientstab " \
              "WHERE idTelegram = '%s'" % idTelegram
