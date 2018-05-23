# -*- coding: utf-8 -*-
from tempdlg_subsystem.temp_logic import CalcDaysModule
from clients_subsystem.rii.database.TimeTableModule import TimeTable


def getText(client):
    this_week = CalcDaysModule.getNumWeek()
    ttList = TimeTable().getTimeTableOnWeek(idClientGroup=client['idClientGroup'],
                                            idClient=client['idRii'],
                                            numWeek=this_week)

    text = "Ваше расписание на эту неделю : \n"
    dayName = ['\nПонедельник\n', '\nВторник\n', '\nСреда\n', '\nЧетверг\n',
               '\nПятница\n', '\nСуббота\n']
    iDay=0
    timeList = CalcDaysModule.getTimeList()
    for dayList in ttList:
        if iDay<6:
            text += dayName[iDay]
            if len(dayList):
                text+"Время \t Дисциплина \t Аудитория \n"
                for j in range(len(dayList)):
                    numLesson = dayList[j]['numLesson']
                    text+="%s \t %s \t %s\n" \
                          % (timeList[numLesson-1], dayList[j]['discipline'],
                             dayList[j]['numAud'])

            else:
                text+="Нет занятий\n"
            iDay += 1
        else:
            break
    return text


def execute(args):
    '''
    Запрос расписания на текущую неделю	
    :param args: кортеж входных параметров,
            args[0] == ссылка на класс шаблонной логики
    :return: Возвращает текстовый ответ в конце сценария
    '''
    tempLogic = args[0]
    client = tempLogic.client

    text = getText(client)
    return text