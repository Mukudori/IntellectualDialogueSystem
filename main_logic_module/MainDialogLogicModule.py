from tempdlg_subsystem.temp_logic.TempDialogModule import TempDialog
from ai_subsystem.lib.chat import ChatWithModel
from main_logic_module.UserMessageModule import UserMessage

class MainDialogLogic(object):
    def __init__(self):
        super().__init__()
        self.clients = []
        self.ai_activated=False
        self.ai_chat=0
        self.stopWord = 'ЗАКОНЧИТЬ_БЕСЕДУ'

    def getAnswerFromMessage(self, message):
        tempLogic = self.checkClient(message)
        tempLogic = tempLogic if tempLogic else self.addClient(message)

        if tempLogic.client['ai_activated']:
            if message.text.upper() == self.stopWord:
                tempLogic.client['ai_activated']=False
                answer='Режим беседы деактивирован.'
                answerData = {'answer': answer, 'executable' : False}
            else:
                answer = self.ai_chat.GetAnswer(message.text)
                answerData = {'answer' : answer[0], 'executable' : False}
            return {'answerData':answerData, 'tempLogic' :  0}
        else:
            answerData=tempLogic.GetAnswer(message.text)
            return {'answerData': answerData, 'tempLogic' : tempLogic}

    def getAnswerFromText(self, text):
        message=UserMessage()
        message.setText(text)
        return self.getAnswerFromMessage(message)



    def addClient(self, message):
        tempLogic = TempDialog(mainLogic=self, telegramMessage=message)
        self.clients.append(tempLogic)
        return tempLogic

    def checkClient(self, message):
        for logic in self.clients:
            if message.from_user.id == logic.client['idTelegram']:
                return logic
        return False

    def startAI(self):
       # try:
            if not self.ai_activated:
                self.ai_activated=True
                self.ai_chat = ChatWithModel()
                self.ai_chat.startSession()


    def executeScrypt(self, client, idAction):

        retText = client['temp_logic'].executeScrypt(idAction)
        return retText

