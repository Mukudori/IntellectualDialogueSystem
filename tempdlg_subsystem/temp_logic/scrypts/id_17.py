# -*- coding: utf-8 -*-
from clients_subsystem.rii.database.ProjectorsModule import Projectors


def getText():

    data = Projectors().getListInfo()

    text = str()#"Название устройства\tМестонахождение\n"
    for row in data:
        text += "%s \t %s \t %s\n" % (row['name'],row['numAud'], row['fioClient'])
    return text


def execute(args):
    '''
	Получение списка проекторов
    :param args: кортеж входных параметров,
            args[0] == ссылка на класс шаблонной логики
    :return: Возвращает текстовый ответ в конце сценария
    '''
    tempLogic = args[0]
    outText = getText()

    return outText