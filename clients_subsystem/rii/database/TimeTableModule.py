from dbConnector import DataBaseModule as DBM
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class TimeTable(object):
    def __init__(self):
        super().__init__()

    def getGroupList(self, idGroup, numDay):
        sql = "SELECT timetable.id as id, timetable.discipline as discipline, " \
              "timetable.numDay as numDay, timetable.numLesson as numLesson, " \
              "clients.shortfio as fioTeacher, audtable.num as numAud " \
              "FROM (riidb.timetable INNER JOIN riidb.clients " \
              "ON timetable.idTeacher = clients.id " \
              "AND timetable.idCathGroup = '%s' " \
              "AND timetable.numDay='%s') " \
              "INNER JOIN riidb.audtable ON audtable.id = timetable.idAud " \
              "ORDER BY timetable.numLesson;" \
              % (idGroup,numDay)
        data = DBM.GetData(sql=sql, nameDB='riidb')
        return data

    def getTeacherList(self, idTeacher, numDay):
        sql = "SELECT timetable.id as id, timetable.discipline as discipline, " \
              "timetable.numDay as numDay, timetable.numLesson as numLesson, " \
              "cathGroup.name as nameGroup, audtable.num as numAud " \
              "FROM (riidb.timetable INNER JOIN riidb.cathGroup ON " \
              "timetable.idCathGroup = cathGroup.id) INNER JOIN riidb.audtable " \
              "ON audtable.id = timetable.idAud " \
              "WHERE timetable.idTeacher = '%s' AND timetable.numDay = '%s' " \
              "ORDER BY timetable.numLesson;" \
               % (idTeacher,numDay)
        data = DBM.GetData(sql=sql, nameDB='riidb')
        return data

    def insertDiscipline(self, idTeacher, idCathGroup, discipline, numDay,
                         numLesson, idAud):
        sql = "INSERT INTO riidb.timetable (idTeacher, idCathGroup, discipline, " \
              "numDay, numLesson, idAud) " \
              "VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" \
              % (idTeacher, idCathGroup, discipline, numDay, numLesson, idAud)
        index = DBM.ExecuteSQL(sql=sql, nameDB='riidb')
        return index

    def updateDiscipline(self, idTimeTable, idTeacher, idCathGroup, discipline, numDay,
                         numLesson, idAud):
        sql = "UPDATE riidb.timetable " \
              "SET idTeacher='%s', idCathGroup='%s', discipline='%s', numDay='%s', " \
              "numLesson='%s', idAud='%s' " \
              "WHERE id='%s'" \
              % (idTeacher, idCathGroup, discipline, numDay, numLesson, idAud, idTimeTable)
        DBM.ExecuteSQL(sql=sql, nameDB='botdb')

    def deleteDiscipline(self, id):
        sql = "DELETE FROM riidb.timetable " \
              "WHERE id = '%s';" % id
        DBM.ExecuteSQL(sql=sql, nameDB='riidb')

    def paddingTable(self, data):
        i=0

        pad = {'discipline': '-', 'fioTeacher' : '-', 'numAud' : '-'}
        while i<(len(data)):
            if i+1!=data[i]['numLesson']:
                pad['numLesson'] = i+1
                data.insert(i, pad)
                continue
            i+=1

    def getStudentsModel(self, idGroup, numDay):
        data = self.getGroupList(idGroup,numDay)

        fieldsView = ['Время', "Дисциплина", "Преподаватель", "Ауд."]
        fieldsTable = ['discipline', 'fioTeacher', 'numAud']
        timelist = ['8:30-10:00',
                    '10:10-11:40',
                    '12:10-13:40',
                    '13:50-15:20',
                    '15:30-17:00',
                    '17:10-18:40']
        self.paddingTable(data)
        model = DBM.CreateTableViewModelFromData(data,fieldsTable, fieldsView, timelist)
        return model

    def getTeacherModel(self, idTeacher, numDay):
        data = self.getTeacherList(idTeacher=idTeacher, numDay=numDay)
        fieldsView = ['Время',"Группа", "Дисциплина", "Ауд."]
        fieldsTable = ['nameGroup', 'discipline', 'numAud']
        timelist = ['8:30-10:00',
                    '10:10-11:40',
                    '12:10-13:40',
                    '13:50-15:20',
                    '15:30-17:00',
                    '17:10-18:40']
        self.paddingTable(data)
        model = DBM.CreateTableViewModelFromData(data, fieldsTable, fieldsView, timelist)
        return model

    def getTimeTableOnWeek(self, idClientGroup, idClient, numWeek):

        if numWeek == 1:
            dayRange = (1, 2, 3, 4, 5, 6)
        else:
            dayRange = (7, 8, 9, 10, 11, 12)
        ttList = []
        if idClientGroup == 2:
            for day in dayRange:
                ttList.append(self.getTeacherList(idTeacher=idClient,
                                                  numDay=day))
        else:
            for day in dayRange:
                ttList.append(self.getGroupList(idGroup=idClient,
                                                  numDay=day))
        return ttList


    def getAudInfo(self, id, numDay, numLesson):
        sql = "SELECT clients.shortfio as teacherFio, timetable.discipline " \
              "as discipline " \
              "FROM riidb.clients INNER JOIN riidb.timetable " \
              "ON clients.id = timetable.idTeacher AND " \
              "timetable.idAud ='%s' AND timetable.numDay='%s' " \
              "AND timetable.numLesson='%s'" \
              % (id, numDay, numLesson)
        data =  DBM.GetData(sql=sql, nameDB='riidb')
        if len(data):
            return data[0]











