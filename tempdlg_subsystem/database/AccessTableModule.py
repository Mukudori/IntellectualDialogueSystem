from tempdlg_subsystem.database import DataBaseModule

class AccessTable:
    def __init__(self):
        self.__Table = 0

    def DeleteRecordFromContextID(self, idGroup, idContext):
        idCon =str(idContext)
        idG = str(idGroup)
        DataBaseModule.ExecuteSQL("""
        DELETE FROM accesstab 
        WHERE idGroup ='""" + idG+"' and idContext = '"+idCon+"';")

    def AddRecord(self, idGroup, idContext):
        idG = str(idGroup)
        idCon = str(idContext)
        id = DataBaseModule.ExecuteSQL("""
         INSERT accesstab (idGroup, idContext) 
         VALUES ('"""+idG+"','"+idCon+"');")

        return id

    def GetIDGroupListFromIDContext(self, idContext):
        data = DataBaseModule.GetData(
            """
            SELECT idGroup FROM accesstab 
            WHERE idContext ='"""+str(idContext)+"';"

        )
        return [rec['idGroup'] for rec in data]

    def DeleteFromContextID(self, idContext):
        DataBaseModule.ExecuteSQL(
            """DELETE FROM accesstab 
            WHERE idContext = '"""+str(idContext)+"';"
        )
