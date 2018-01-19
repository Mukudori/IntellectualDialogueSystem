import DataBaseModule

class WordTable:
    '''    Класс словаря с одним обращением к БД для чтения.
        Все операции проводятся с кортежом
    '''
    def __init__(self):
        self.WordsBook = DataBaseModule.GetData('SELECT * FROM wordtab')

    def GetWordFromID(self, id):
        for record in self.WordsBook:
            if id == record['id']:
                return record['word']
        return '<id = '+str(id)+' не найден>'

    def GetDecodeText(self, inp):
        inpList = inp.split(';')
        outText = str()
        for string in inpList:
            if (string != str()):
                wordS = str()
                i=0
                while i < len(string):
                    if (string[i]>='0' and string[i]<='9'):
                        while (i < len(string) and string[i] >= '0' and string[i] <= '9'):
                            wordS+=string[i]
                            i += 1

                    if wordS != str():
                        outText+=self.GetWordFromID(int(wordS))
                        wordS=str()

                    if i<len(string):
                        outText+=string[i]
                    i+=1
                outText+=';'
        return outText

    def FindWord(self, word):
        for record in self.WordsBook:
            if record['word'] == word.upper():
                return 1
        return 0

    def CheckString(self, text):
        TEXT = text.upper()
        word = str()
        for i in range(len(TEXT)):
            if(TEXT[i]>='А' and TEXT[i]<='Я'):
                word+=TEXT[i]
            else:
                if (len(word)):
                    if (not self.FindWord(word)):
                        return [0,word]
                    else:
                        word=str()
        if (len(word)):
            if (not self.FindWord(word)):
                return [0, word]
        return [1,0]








    def DeleteWordFromID(self, id):
        pass

    def AppendWord(self, word):
        pass