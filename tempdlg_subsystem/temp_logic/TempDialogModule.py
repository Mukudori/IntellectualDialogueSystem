# -*- coding: utf-8 -*-
from tempdlg_subsystem.database.ContextTableModule import ContextTable
from tempdlg_subsystem import StringFunctionsModule
from tempdlg_subsystem.database.AnswerTableModule import AnswerTable
import random
from tempdlg_subsystem.database.ActionTableModule import ActionTable
from tempdlg_subsystem.temp_logic.scrypts import ExecuteScryptsModule


class TempDialog:
    '''
     Модуль шаблонной логики.

     При инициализации принимает 2 аргумента:
     idGroup - идентефикатор группы пользователей
               по умолчанию равен 4 (Гость)

     mainLogic - ссылка на основной модуль логики,
                для обмена информацией между модулями.

     Снаружи модуля должен использоваться только метод
     GetAnswer, который принимает текстовую строку и выдает
     ответ с учетом предыдущего контекста.
    '''
    def __init__(self,client, mainLogic):
        self.conTab = ContextTable()
        self.idGroup = client['id_Group']
        self.CurrentContextLevel = 0
        self.CurrentContextID = 0
        self.FindedContext = False
        self.mainLogic = mainLogic
        self.client=client
        self.carrentMessage = 0

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
                    w=row['question'].upper()

                    if word in w.upper():
                        check+=1
                        id =row['idQ']
                        lenQ =len(StringFunctionsModule.GetWordsListFromTextWithRE(row['question']))
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
        contextIDTup = [{'id' : 0 , 'level' : 0, 'idParent' : 0},] #инициализация кортежа словарей
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
                self.carrentMessage = random.choice(AnswerTable().GetAnswerDictFromContextID(self.CurrentContextID))

                return self.carrentMessage
            elif self.CurrentContextLevel:
                curCon = self.conTab.GetIDParent(self.CurrentContextID, self.idGroup)[0]
                self.CurrentContextID = curCon['id']
                self.CurrentContextLevel = curCon['level']
            else:
                break

        retError = random.choice(
                [
                    'Я вас не понимаю.',
                    'Неизвестная команда.'
                ]
            )
        self.carrentMessage = {'answer': retError, 'idAction' : 0, 'executable' : False}
        return self.carrentMessage

    def сheckAction(self, idAction):
        actionRec = ActionTable().CheckScryptFromIDAction(idAction)
        if actionRec:
            #print()[str(actionRec)].GetAnswer()
            text = ExecuteScryptsModule.GetAnswer('id_'+str(idAction),
                                                  self)
            if text:
                return '\n\n' +text
            else:
                return 'Сценарий выполнен'
        return False

    def startAI(self):
        self.client['ai_activated'] = True
        self.mainLogic.startAI()

















