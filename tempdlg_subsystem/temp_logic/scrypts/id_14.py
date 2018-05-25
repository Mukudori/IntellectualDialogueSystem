# -*- coding: utf-8 -*-
from tempdlg_subsystem.OtherClasses.WebPagesDataModule import WebPageData


def getText():
    webList = WebPageData().getList()
    n = len(webList)
    if n>3:
        n-=3
        webList = webList[n::1]

    text = str()
    for row in webList:
        text+="\nДата : %s \n" \
              "Заголовок : %s \n" \
              "Ссылка : %s\n" \
              % (row['date'], row['title'], row['url'])
    return text


def execute(args):
    '''
        ЗАПРОС ПОСЛЕДНИХ 3-х НОВОСТЕЙ
    :param args: кортеж входных параметров,
            args[0] == ссылка на класс шаблонной логики
    :return: Возвращает текстовый ответ в конце сценария
    '''
    #tempLogic = args[0]
    text = getText()
    return text