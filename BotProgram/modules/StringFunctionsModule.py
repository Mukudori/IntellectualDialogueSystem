from itertools import groupby

def GetWordsListFromText(text):
    # Вернуть слова, содержащиеся в строке, в верхнем регистре
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

    return [word for word, _ in groupby(wordsList)]


