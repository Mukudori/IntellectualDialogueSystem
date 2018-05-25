# -*- coding: utf-8 -*-
from clients_subsystem.rii.database.AuditoryModule import Auditory
import re
from tempdlg_subsystem.temp_logic import CalcWorkDaysModule as CWDM


def getNum(text):
    #num = str()
    p = re.compile(u'[0-9]+', re.S)
    ret = p.findall(text.upper())
    if len(ret):
        return ret[0]

def getAudInfo(num):
    numDay=CWDM.getWeekDay()
    numLesson = CWDM.getNumLesson()
    print(numDay)
    if numLesson:
        audInfo= Auditory().getAuditoryInfo(numAud=num,
                                            numDay=numDay,
                                            numLesson=numLesson)
        return audInfo

def createTextInfo(audInfo):

    text = "В данный момент аудитория занята.\n" \
           "Сейчас там идет пара '%s' у преподавателя %s" \
           % (audInfo['discipline'], audInfo['teacherFio'])
    return text



def getText(client):
    text = client['message'].text
    num = getNum(text)
    if num:
        text = "Вы запросили %s аудиторию;\n" % num
        audInfo = getAudInfo(num)
        if audInfo:
            text += createTextInfo(audInfo)
        else:
            text += "В данный момент аудитория свободна."
    else:
        text = "Аудитория введена некорректно."
    return text


def execute(args):
    '''
    Проверка свободной аудитории СЕЙЧАС
    :param args: кортеж входных параметров,
            args[0] == ссылка на класс шаблонной логики
    :return: Возвращает текстовый ответ в конце сценария
    '''
    tempLogic = args[0]

    return getText(tempLogic.client)