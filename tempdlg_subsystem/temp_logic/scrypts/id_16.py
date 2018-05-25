# -*- coding: utf-8 -*-
from clients_subsystem.rii.database.AuditoryModule import Auditory
import re

def getAudInfo(numAud, numDay, numLesson):
    if numLesson:
        audInfo= Auditory().getAuditoryInfo(numAud=numAud,
                                            numDay=numDay,
                                            numLesson=numLesson)
        return audInfo

def getNum(text):
    p = re.compile(u'[0-9]+', re.S)
    ret = p.findall(text.upper())
    if len(ret):
        return ret

def createTextInfo(audInfo):

    text = "В указанное время там идет пара '%s' у преподавателя %s" \
           % (audInfo['discipline'], audInfo['teacherFio'])
    return text

def getText(client):
    text = client['message'].text
    nums = getNum(text)
    if len(nums) ==3:
        numAud, numDay, numLesson = (num for num in nums)
        text = "Вы запросили %s аудиторию на %s день, %s пару;\n" \
               % (numAud,numDay,numLesson)
        audInfo = getAudInfo(numAud, numDay, numLesson)
        if audInfo:
            text += createTextInfo(audInfo)
        else:
            text += "В указанное время аудитория свободна."
    else:
        text = "Не могу обработать ваш запрос. \nВведите, пожалуйста в виде " \
               "'<номер аудитории> аудитория на <номер дня> день <номер пары> пару.\n" \
               "Напоминаю, что учебные дни нумируются от 1 до 12."
    return text

def execute(args):
    '''
    Проверка свободной аудитории (день, пара)
    :param args: кортеж входных параметров,
            args[0] == ссылка на класс шаблонной логики
    :return: Возвращает текстовый ответ в конце сценария
    '''
    tempLogic = args[0]

    return getText(tempLogic.client)