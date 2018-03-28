# -*- coding: utf-8 -*-
from itertools import groupby
import re

def GetWordsListFromText(text):
    # Вернуть слова, содержащиеся в строке, в верхнем регистре
    # ИСПОЛЬЗОВАТЬ НЕ ЖЕЛАТЕЛЬНО
    textU = text.upper()
    wordsList = list()
    i = 0
    while i < len(textU):
        word = str()
        while i < len(textU) and textU[i] >= 'А' and textU[i] <= 'Я':
            word += textU[i]
            i += 1
        if len(word):
            wordsList.append(word)
        else:
            i += 1

    return [word for word, _ in groupby(wordsList)] # возвращается список без повторов

def GetWordsListFromTextWithRE(text):
    # Более грамотный способ выделения списка слов
    # через регулярное выражение
    if type(text) == type(u''):
        p = re.compile(u'[А-Я]+', re.S)
        ret = p.findall(text.upper())#.encode('UTF-8'))
    else:
        p = re.compile('[А-Я]+', re.S)
        buf = p.findall(text.upper())
        ret = [word.decode('UTF-8') for word in buf]
    return ret



