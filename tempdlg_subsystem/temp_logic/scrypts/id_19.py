# -*- coding: utf-8 -*-

from clients_subsystem.rii.database.ProjectorsModule import Projectors

def getText(client):

    try:
        device = Projectors().returnToCath(idClient=client['idRii'])
        if device:
            return "Проектор '%s' отмечен как возвращенный на кафедру" % device
        else:
            return "За вами не зарезервировано проекторов"
    except:
        return "Произошла ошибка при выполнении запроса"


def execute(args):
    '''
    Сдача проектора на кафедру
    :param args: кортеж входных параметров,
            args[0] == ссылка на класс шаблонной логики
    :return: Возвращает текстовый ответ в конце сценария
    '''
    tempLogic = args[0]
    client = tempLogic.client

    outText = getText(client)

    return outText