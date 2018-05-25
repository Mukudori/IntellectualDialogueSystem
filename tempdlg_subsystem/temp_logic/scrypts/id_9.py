# -*- coding: utf-8 -*-
from tempdlg_subsystem.temp_logic import CalcWorkDaysModule
from clients_subsystem.rii.database.TimeTableModule import TimeTable


def getTTforTeacher(client):
    numDay = CalcWorkDaysModule.getWeekDay()
    idClient = client['idRii']
    ttList = TimeTable().getTeacherList(idTeacher=idClient,
                                        numDay=numDay)

    return ttList

def getTTforStudent(client):
    numDay = CalcWorkDaysModule.getWeekDay()
    idClient = client['idRii']
    ttList = TimeTable().getGroupList(idGroup=idClient,
                                      numDay=numDay)
    return ttList

def createViewString(client):
    if client['idClientGroup'] == 2:
        ttList = getTTforTeacher(client)
    else:
        ttList = getTTforStudent(client)

    if len(ttList):
        timeList = CalcWorkDaysModule.getTimeList()
        text = "Ваше раписание на сегодня : \n" \
               "Время \t Дисциплина \t Аудитория \n"
        for i in range(len(ttList)):
            text+="%s, \t %s, \t %s;\n" \
                  % (timeList[ttList[i]['numLesson']-1], ttList[i]['discipline'],
                     ttList[i]['numAud'])
    else:
        text = "У вас нет сегодня занятий."
    return text

def execute(args):
    '''
    ЗАПРОС РАСПИСАНИЯ НА ДЕНЬ
    :param args: кортеж входных параметров,
            args[0] == ссылка на класс шаблонной логики
    :return: Возвращает текстовый ответ в конце сценария
    '''
    tempLogic = args[0]
    client = tempLogic.client
    text = createViewString(client)
    return text


    