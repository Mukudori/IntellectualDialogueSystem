# -*- coding: utf-8 -*-

def getText(client):

    """
    Функция обрабатывающая запрос
    :param client:
    :return:
    """


def execute(args):
    '''
    Основная функция запуска сценария
    :param args: кортеж входных параметров,
            args[0] == ссылка на класс шаблонной логики
    :return: Возвращает текстовый ответ в конце сценария
    '''
    tempLogic = args[0]
    client = tempLogic.client

    outText = getText(client)

    return outText