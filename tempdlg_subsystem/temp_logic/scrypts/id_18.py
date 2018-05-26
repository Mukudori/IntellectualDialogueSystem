# -*- coding: utf-8 -*-
from tempdlg_subsystem import StringFunctionsModule as SFM
from clients_subsystem.rii.database.ProjectorsModule import Projectors


def getText(client):
    message = SFM.GetWordsListFromTextWithRE(client['message'].text)
#    try:
    nameProj = message[1]
    numAud = message[3]
    ret = Projectors().reserveDevice(nameDevice=nameProj,
                                         numAud=numAud,
                                         idClient=client['idRii'])
    return ret['text']


    """except:
        return "Не могу обработать ваш запрос. Введите его в форме " \
               "'Резервирую <имя устройства> в <номер аудитории> ауд"
"""





def execute(args):
    '''
    Резервирование проектора
    :param args: кортеж входных параметров,
            args[0] == ссылка на класс шаблонной логики
    :return: Возвращает текстовый ответ в конце сценария
    '''
    tempLogic = args[0]
    client = tempLogic.client

    outText = getText(client)

    return outText