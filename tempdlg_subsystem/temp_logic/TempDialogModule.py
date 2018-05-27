# -*- coding: utf-8 -*-
from tempdlg_subsystem.database.ContextTableModule import ContextTable
from tempdlg_subsystem import StringFunctionsModule as SFM
from tempdlg_subsystem.database.AnswerTableModule import AnswerTable
import random
from tempdlg_subsystem.database.ActionTableModule import ActionTable
from tempdlg_subsystem.temp_logic.scrypts import ExecuteScryptsModule
from tempdlg_subsystem.database.ClientTabModule import ClientsTab
from main_logic_module.LogsSaverModule import LogsSaver


class TempDialog:
    '''
     Модуль шаблонной логики.

     При инициализации принимает 2 аргумента:
     telegramMessage - сообщение из телеграма, содержащее
                        информацию о клиенте.

     mainLogic - ссылка на основной модуль логики,
                для обмена информацией между модулями.

     Снаружи модуля должен использоваться только метод
     GetAnswer, который принимает текстовую строку и выдает
     ответ с учетом предыдущего контекста.
    '''
    def __init__(self,mainLogic, telegramMessage=0, logging=True):
        self.mainLogic = mainLogic
        self.setupPars(logging)
        self.initClient(telegramMessage)


    def setupPars(self, logging):
        self.conTab = ContextTable()
        self.CurrentContextLevel = 0
        self.CurrentContextID = 0
        self.FindedContext = False
        self.carrentMessage = 0
        self.permissibleError = 1.5
        self.logsSaver = LogsSaver()
        self.logging =logging


    def FuncCoefError(self, check, lenText, lenQ):
        if lenText and lenQ:
            p = check/lenText if check<lenText else lenText/check
            q = check/lenQ if check<lenQ else lenQ/check
            return p + q
        else:
            return 0

    def compare(self, word, wordQuestion):

        w = word.upper()
        wList = wordQuestion
        for wq in wList:
            if w in wq:
                return True
            elif wq == 'NUM' and SFM.isint(w):
                return True
        #elif wq == 'STR':
            #return True

        return False

    def FindQuestionInContext(self, question, idContext):
        questionDict = self.conTab.GetQuestionDictFromContextID(idContext=idContext,
                                                                idGroup=self.client['idClientGroup'])
        if questionDict != None:
            WordList = SFM.GetWordsListFromTextWithRE(question)
            checkCoef = 0
            checkID = 0
            for row in questionDict:
               # if row['idQ'] == 67:
               #     print('bug')
                check=0
                id=0
                lenQ=0
                for word in WordList:

                    wq=SFM.GetWordsListFromTextWithRE(row['question'])
                    if self.compare(word,wq):
                        check+=1
                        id =row['idQ']
                        lenQ =len(SFM.GetWordsListFromTextWithRE(row['question']))
                check = self.FuncCoefError(check=check, lenText=len(WordList), lenQ=lenQ)
                if check>checkCoef and check>self.permissibleError:
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
                parentTup = self.conTab.GetIDDictFromLevel(0, self.client['idClientGroup'])
            else:
                parentTup = self.conTab.GetIDParent(self.CurrentContextID, self.client['idClientGroup'])


            if parentTup:

                contextIDTup+=parentTup
            #Средний уровень
            currentParent = self.conTab.GetIDParent(self.CurrentContextID, self.client['idClientGroup'])
            broTup = self.conTab.GetChildContextIDList(currentParent[0]['id'], self.client['idClientGroup'])

            if broTup:
                contextIDTup+=broTup

            #Нижний уровень
            childTup = self.conTab.GetChildContextIDList(self.CurrentContextID, self.client['idClientGroup'])

            if childTup:
                contextIDTup+=childTup

        else:
            contextIDTup = self.conTab.GetIDDictFromLevel(0, self.client['idClientGroup'])
            self.CurrentContextLevel = 0
            childTup = self.conTab.GetChildContextIDList(self.CurrentContextID, self.client['idClientGroup'])

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

        #print("er = %s"%errorQ)
        return idQ

    def GetAnswer(self, question):
        """Ищем пока не нактнемся на вопрос в рамках текущей ветви контестов
        Или пока не пройдемся по всем доступным вопросам ветви"""
        while True:
            idQ = self.GetQuestionID(question)
            if idQ:
                self.carrentMessage = random.choice(
                    AnswerTable().GetAnswerDictFromContextID(
                        self.CurrentContextID))
                self.carrentMessage = {**self.carrentMessage, **{'error': 0} }

                return self.carrentMessage
            elif self.CurrentContextLevel:
                curCon = self.conTab.GetIDParent(self.CurrentContextID,
                                                 self.client['idClientGroup'])[0]
                self.CurrentContextID = curCon['id']
                self.CurrentContextLevel = curCon['level']
            else:
                break

        retError = random.choice(
                [
                    'Я вас не понимаю.\n'
                    'Если выхотите перейти в режим беседы, '
                    'то введите "давай побеседуем".',
                    'Неизвестная команда.'
                ]
            )
        self.carrentMessage = {'answer': retError, 'idAction' : 0,
                               'executable' : False, 'error' : 1}
        return self.carrentMessage

    def executeScrypt(self, idAction):
        actionRec = ActionTable().CheckScryptFromIDAction(idAction)
        if actionRec:
            #print()[str(actionRec)].GetAnswer()
            text = ExecuteScryptsModule.GetAnswer('id_'+str(idAction),
                                                  self)
            if text:
                ret = text
            else:
                ret = 'Сценарий выполнен'
        else:
            ret = "Сценарий не выполнен"
        if self.logging:
            self.logsSaver.saveAllLog(client=self.client,
                                      answer=ret,
                                      error=0)
        return ret

    def startAI(self):
        self.client['ai_activated'] = True
        self.mainLogic.startAI()

    def initClient(self, message):
        if message:
            rec = ClientsTab().getInfoFromIDTelegram(
                idTelegram=message.from_user.id)
            if rec:
                rec['idTelegram'] = message.from_user.id
                rec['first_name'] = message.from_user.first_name
                rec['last_name'] = message.from_user.last_name
                rec['username'] = message.from_user.username
                rec['ai_activated'] = False
                rec['args'] = []
                if message.from_user.id == 1:
                    rec['idClientGroup'] = 1




            else:
                rec = dict()
                rec['idTelegram'] = message.from_user.id
                rec['first_name'] = message.from_user.first_name
                rec['last_name'] = message.from_user.last_name
                rec['username'] = message.from_user.username
                rec['ai_activated'] = False
                rec['idClientGroup'] = 4
                rec['args'] = []
        else:
            rec = dict()
            rec['idTelegram'] = 0
            rec['first_name'] = '-'
            rec['last_name'] = '-'
            rec['username'] = '-'
            rec['ai_activated'] = False
            rec['idClientGroup'] = 4
            rec['args'] = []
        rec['message'] = message

        self.client = rec

















