from dbConnector import DataBaseModule



class Client(object):
    def __init__(self):
       super().__init__()

    def getFromID(self, id):
        sql = "SELECT id as idClient, fio, shortfio, idClientGroup,\
           idInfo FROM riidb.clients WHERE id='%s';"%str(id)

        rec = DataBaseModule.GetData(nameDB='riidb', sql=sql)
        if len(rec):
            rec = rec[0]
            if rec['idClientGroup'] == 3:
                sql = "SELECT id as idCathGroup, name as nameCathGroup, cource," \
                      " idCathedra, idCurator FROM riidb.cathGroup " \
                      "WHERE id='%s';"%str(rec['idClientGroup'])
            else:
                sql = "SELECT teacherinfo.dolzhnost as dozhnost, teacherinfo.obrazovanie " \
                      "as obrazovanie, teacherinfo.stepen as stepen, teacherinfo.zvanie " \
                      "as zvanie, teacherinfo.kvalifikacia as kvalifikacia, teacherinfo.idCath " \
                      "as idCath, cathedra.name as nameCath " \
                      "FROM riidb.teacherinfo INNER JOIN riidb.cathedra " \
                      "ON teacherinfo.idCath = cathedra.id" \
                      " WHERE teacherinfo.id='%s';"%rec['idInfo']
            rec = {**rec, **DataBaseModule.GetData(nameDB='riidb', sql=sql)[0]}
            return rec

    def getStudentsList(self):
        sql = "SELECT clients.id as id, clients.fio as fio, " \
              "clients.idClientGroup, " \
              "cathGroup.name as cathGroup, cathGroup.course as course " \
              "FROM riidb.clients INNER JOIN riidb.cathGroup " \
              "ON clients.idInfo = cathGroup.id and clients.idClientGroup=3;"
        data= DataBaseModule.GetData(nameDB='riidb', sql=sql)[0]
        return data

    def getTeachersList(self):
        pass

    def getTVTeachersModel(self, idCathedra=0):
        if not idCathedra:
            sql = "SELECT clients.id as id, clients.fio as fio, " \
            "teacherinfo.dolzhnost as dolzhnost, teacherinfo.obrazovanie as obrazovanie, " \
            "teacherinfo.stepen as stepen, teacherinfo.zvanie as zvanie, " \
            "teacherinfo.kvalifikacia as kvalifikacia, " \
            "cathedra.name as cathedra " \
            "FROM (riidb.clients INNER JOIN riidb.teacherinfo " \
            "ON clients.idInfo = teacherinfo.id and clients.idClientGroup=2) " \
            "INNER JOIN riidb.cathedra ON cathedra.id = teacherinfo.idCath;"
        else:
            sql = "SELECT clients.id as id, clients.fio as fio, " \
                  "teacherinfo.dolzhnost as dolzhnost, teacherinfo.obrazovanie as obrazovanie, " \
                  "teacherinfo.stepen as stepen, teacherinfo.zvanie as zvanie, " \
                  "teacherinfo.kvalifikacia as kvalifikacia, " \
                  "cathedra.name as cathedra " \
                  "FROM (riidb.clients INNER JOIN riidb.teacherinfo " \
                  "ON clients.idInfo = teacherinfo.id and clients.idClientGroup=2 ) " \
                  "INNER JOIN riidb.cathedra ON cathedra.id = teacherinfo.idCath " \
                  "AND teacherinfo.idCath = '%s';" % idCathedra

        nameList = ['id', 'fio', 'dolzhnost', 'obrazovanie', 'stepen',
                    'zvanie', 'kvalifikacia', 'cathedra']
        asList = ['id', 'ФИО', 'Должность', 'Образование', "Степень",
                  "Звание", "Квалификация", "Кафедра"]
        model = DataBaseModule.CreateTableViewModel(sql, nameList, asList, nameDB='riidb')
        return model

    def getTVStudentsModel(self, cathGroup=0):
        if cathGroup == 0:
            sql = "SELECT clients.id as id, clients.fio as fio, " \
                  "clients.idClientGroup, " \
                  "cathGroup.name as cathGroup, cathGroup.course as course " \
                  "FROM riidb.clients INNER JOIN riidb.cathGroup " \
                  "ON clients.idInfo = cathGroup.id and clients.idClientGroup=3;"
        else:
            sql = "SELECT clients.id as id, clients.fio as fio, " \
                  "clients.idClientGroup, " \
                  "cathGroup.name as cathGroup, cathGroup.course as course " \
                  "FROM riidb.clients INNER JOIN riidb.cathGroup " \
                  "ON clients.idInfo = cathGroup.id and clients.idClientGroup=3 " \
                  "and clients.idInfo='%s';"%cathGroup

        nameList = ['id', 'fio', 'cathGroup', 'course']
        asList = ['id', 'ФИО', 'Группа', 'Курс']
        model = DataBaseModule.CreateTableViewModel(sql, nameList, asList,
                                                    nameDB='riidb')
        return model

    def _insertRecord(self, fio, shortfio, idInfo, idClientGroup=3):
        sql = "INSERT INTO riidb.clients (fio, shortfio, idInfo, idClientGroup) " \
              "VALUES ('%s', '%s','%s', '%s')" % (fio, shortfio,str(idInfo), str(idClientGroup))
        idClient = DataBaseModule.ExecuteSQL(sql=sql, nameDB='riidb')
        return idClient

    def insertStudent(self, shortfio, fio, idInfo):
        idClient = self._insertRecord(fio,shortfio,idInfo, idClientGroup=3)
        return idClient

    def insertTeacher(self, fio, shortfio, dolzhnost, obrazovanie, stepen, zvanie,
                      kvalifikacia, idCath):
        sql = "INSERT INTO riidb.teacherinfo (dolzhnost,obrazovanie,stepen," \
              "zvanie,kvalifikacia, idCath) " \
              "VALUES ('%s','%s','%s','%s','%s','%s');"%\
              (dolzhnost, obrazovanie, stepen, zvanie, kvalifikacia, idCath)
        idInfo = DataBaseModule.ExecuteSQL(sql=sql, nameDB='riidb')
        if idInfo:
            idClient =  self._insertRecord(fio,shortfio,idInfo, idClientGroup=2)
            return idClient
        else:
            return 0

    def _updateRecord(self, id, fio, shortfio, idInfo=0):
        if idInfo:
            sql = "UPDATE riidb.clients " \
                  "SET fio='%s', shortfio='%s', idInfo='%s' " \
                  "WHERE id='%s';"%(fio,shortfio,idInfo,id)
        else:
            sql = "UPDATE riidb.clients " \
                  "SET fio='%s', shortfio='%s' " \
                  "WHERE id='%s';" % (fio,shortfio, id)
        DataBaseModule.ExecuteSQL(sql=sql, nameDB='riidb')

    def updateStudent(self, idClient, fio, shortfio, idInfo):
        self._updateRecord(idClient,fio, shortfio,idInfo)

    def updateTeacher(self, idClient, fio, shortfio, dolzhnost, obrazovanie, stepen,
                      zvanie, kvalifikacia, idCath):
        idInfo = self.getFromID(idClient)['idInfo']
        sql = "UPDATE riidb.teacherinfo " \
              "SET dolzhnost='%s', obrazovanie='%s', stepen='%s', zvanie='%s', " \
              "kvalifikacia='%s', idCath='%s' " \
              "WHERE id='%s';"%(dolzhnost,obrazovanie,stepen,zvanie,
                                kvalifikacia,idCath, idInfo)
        DataBaseModule.ExecuteSQL(sql,'riidb')
        self._updateRecord(idClient,fio, shortfio)

    def _deleteRecord(self, id):
        sql = "DELETE FROM riidb.clients " \
              "WHERE id ='%s'"%str(id)
        DataBaseModule.ExecuteSQL(sql=sql, nameDB='riidb')


    def deleteTeacher(self, id):
        record = self.getFromID(id)
        self._deleteRecord(record['idClient'])
        if record['idClientGroup'] == 2:
            sql = "DELETE FROM riidb.teacherinfo " \
                  "WHERE id ='%s'"%record['idInfo']
            DataBaseModule.ExecuteSQL(sql=sql, nameDB='riidb')

    def deleteStudent(self, id):
        self._deleteRecord(id)

    def getTeachersListFromIDCath(self, idCath):
        sql = "SELECT clients.id as id, clients.shortfio as shortfio " \
              "FROM riidb.clients INNER JOIN riidb.teacherinfo " \
              "ON clients.idInfo = teacherinfo.id " \
              "WHERE clients.idClientGroup=2 and " \
              "teacherinfo.idCath='%s';" % idCath
        data = DataBaseModule.GetData(sql=sql, nameDB='riidb')
        return data

    def getStudentsListFromIDCathGroup(self, idCathGroup):
        sql = "SELECT id, fio " \
              "FROM riidb.clients " \
              "WHERE idInfo='%s';" % idCathGroup
        data = DataBaseModule.GetData(sql=sql, nameDB='riidb')
        return data

