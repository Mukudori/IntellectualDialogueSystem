from modules.database.ContextTableModule import ContextTable
from modules import StringFunctionsModule
from modules.database.AnswerTableModule import AnswerTable
import random



class BotDialog:
    def __init__(self, idGroup=4):
        self.conTab = ContextTable()
        self.idGroup = idGroup
        self.CurrentContextLevel = 0
        self.CurrentContextID = 0

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
        idQ = 0
        errorQ = 0

        if self.CurrentContextLevel:
            contextDict = self.conTab.GetChildContextIDList(self.CurrentContextID)
        else:
            contextDict = self.conTab.GetIDDictFromLevel(0)

        for idContext in contextDict:
            idq, er = self.FindQuestionInContext(idContext=idContext['id'], question=question)
            if er > errorQ:
                errorQ = er
                idQ = idq
                self.CurrentContextID = idContext['id']
            childContextDict = self.conTab.GetChildContextIDList(idContext['id'])
            for idChildContext in childContextDict:
                idq, er = self.FindQuestionInContext(idContext=idChildContext['id'], question=question)
                if er > errorQ:
                    errorQ = er
                    idQ = idq
                    self.CurrentContextID = idChildContext['id']
        return idQ


    def GetAnswer(self, question):
        idQ = self.GetQuestionID(question)
        if idQ:
            answerTup = random.choice(AnswerTable().GetAnswerDictFromContextID(self.CurrentContextID))
            return answerTup['answer']
        else:
            return random.choice(
                [
                    'Я вас не понимаю.',
                    'Неизсевстная команда'
                ]
            )








