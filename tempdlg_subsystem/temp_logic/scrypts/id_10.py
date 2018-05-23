# -*- coding: utf-8 -*-
from tempdlg_subsystem.temp_logic import CalcDaysModule


def execute(args):
    '''
    Считает какая по счету сейчас неделя. 
    Первая неделя это 1 февраля
    :param args: кортеж входных параметров,
            args[0] == ссылка на класс шаблонной логики
    :return: Возвращает текстовый ответ в конце сценария
    '''
    num_week = CalcDaysModule.getNumWeek()
    return "Сейчас идет %s неделя." % num_week