from modules.database.ContextTableModule import ContextTable
from modules import StringFunctionsModule
from modules.database.AnswerTableModule import AnswerTable
import random
from modules.database.ActionTableModule import ActionTable
from modules.bot.scrypts import ExecuteScryptsModule
from modules.bot.scrypts import *




class BotDialog:
    def __init__(self, idGroup=4):
        self.conTab = ContextTable()
        self.idGroup = idGroup
        self.CurrentContextLevel = 0
        self.CurrentContextID = 0
        self.FindedContext = False

    def FuncCoefError(self, check, lenText, lenQ):
        if lenText and lenQ:
            return check/lenText + check/lenQ
        else:
            return 0

    def FindQuestionInContext(self, question, idContext):
        questionDict = self.conTab.GetQuestionDictFromContextID(idContext=idContext,
                                                                idGroup=self.idGroup)
        if questionDict != None:
            WordList = StringFunctionsModule.GetWordsListFromTextWithRE(question)
            checkCoef = 0
            checkID = 0
            for row in questionDict:
                check=0
                id=0
                lenQ=0
                for word in WordList:
                    if word in row['question'].upper():
                        check+=1
                        id =row['idQ']
                        lenQ =len(StringFunctionsModule.GetWordsListFromText(row['question']))
                check = self.FuncCoefError(check=check, lenText=len(WordList), lenQ=lenQ)
                if check>checkCoef:
                    checkCoef=check
                    checkID=id
            return [checkID, checkCoef]
        return [0,0]

    def GetQuestionID(self, question):
        idQ = 0 #id вопроса с минимальной ошибкой
        errorQ = 0 # значение минимальной ошибки

        #Проверка предыдущего контекста
        contextIDTup = ({'id' : 0 , 'level' : 0, 'idParent' : 0},) #инициализация кортежа словарей
        if self.CurrentContextID and self.CurrentContextLevel:
            #Верхний уровень
            """ Если уровень 1, то грузим весь верхний уровень,
            иначе только родительский уровень текущего контекста"""
            if self.CurrentContextLevel == 1:
                parentTup = self.conTab.GetIDDictFromLevel(0, self.idGroup)
            else:
                parentTup = self.conTab.GetIDParent(self.CurrentContextID, self.idGroup)


            if parentTup:
                contextIDTup+=parentTup
            #Средний уровень
            currentParent = self.conTab.GetIDParent(self.CurrentContextID, self.idGroup)
            broTup = self.conTab.GetChildContextIDList(currentParent[0]['id'], self.idGroup)

            if broTup:
                contextIDTup+=broTup

            #Нижний уровень
            childTup = self.conTab.GetChildContextIDList(self.CurrentContextID, self.idGroup)

            if childTup:
                contextIDTup+=childTup

        else:
            contextIDTup = self.conTab.GetIDDictFromLevel(0, self.idGroup)
            self.CurrentContextLevel = 0
            childTup = self.conTab.GetChildContextIDList(self.CurrentContextID, self.idGroup)

            if childTup:
                contextIDTup += childTup

        #Проходим по контекстам и ищем совпадения в их вопросах
        for idContext in contextIDTup:

            idq, er = self.FindQuestionInContext(idContext=idContext['id'], question=question)
            if er > errorQ:
                errorQ = er
                idQ = idq
                self.CurrentContextID = idContext['id']
                self.CurrentContextLevel = idContext['level']
            if idContext['idParent']:
                idq, er = self.FindQuestionInContext(idContext=idContext['idParent'], question=question)
                if er > errorQ:
                    errorQ = er
                    idQ = idq
                    self.CurrentContextID = idContext['id']
                    self.CurrentContextLevel = idContext['level']


        return idQ

    def GetAnswer(self, question):
        """Ищем пока не нактнемся на вопрос в рамках текущей ветви контестов
        Или пока не пройдемся по всем доступным вопросам ветви"""
        while True:
            idQ = self.GetQuestionID(question)
            if idQ:
                answerTup = random.choice(AnswerTable().GetAnswerDictFromContextID(self.CurrentContextID))

                answer = answerTup['answer']+self.CheckAction(answerTup['idAction'])
                return answer
            elif self.CurrentContextLevel:
                curCon = self.conTab.GetIDParent(self.CurrentContextID, self.idGroup)[0]
                self.CurrentContextID = curCon['id']
                self.CurrentContextLevel = curCon['level']
            else:
                break


        return random.choice(
                [
                    'Я вас не понимаю.',
                    'Неизвестная команда.'
                ]
            )

    def CheckAction(self, idAction):
        actionRec = ActionTable().CheckScryptFromIDAction(idAction)
        if actionRec:
            print()#[str(actionRec)].GetAnswer()
            return '\n\n'+ExecuteScryptsModule.GetAnswer('id_'+str(idAction))
        return str()












