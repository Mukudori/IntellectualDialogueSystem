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
        client = self.checkClient(message)
        client = client if client else self.addClient(message)

        if client['ai_activated']:
            if message.text.upper() == self.stopWord:
                client['ai_activated']=False
                answer='Режим беседы деактивирован.'
                answerData = {'answer': answer, 'executable' : False}
            else:
                answer = self.ai_chat.GetAnswer(message.text)
                answerData = {'answer' : answer[0], 'executable' : False}
            return [answerData, 0]
        else:
            answerData=client['temp_logic'].GetAnswer(message.text)
            return [answerData, client]

    def getAnswerFromText(self, text):
        message=UserMessage()
        message.setText(text)
        return self.getAnswerFromMessage(message)

    def addClient(self, message):
        client = self.getUserFromDB(message)
        self.clients.append(client)
        return client

    def checkClient(self, message):
        for client in self.clients:
            if message.from_user.id == client['user_id']:
                return client
        return False

    def startAI(self):
       # try:
            if not self.ai_activated:
                self.ai_activated=True
                self.ai_chat = ChatWithModel()
                self.ai_chat.startSession()

    def getUserFromDB(self, message=0):
        clientFounded = False
        if not clientFounded:
            client = dict()
            client['user_id'] = message.from_user.id
            client['first_name'] = message.from_user.first_name
            client['last_name'] = message.from_user.last_name
            client['username'] = message.from_user.username
            client['ai_activated'] = False
            client['id_Group'] = 4
            client['temp_logic'] = TempDialog(mainLogic=self, client=client)
            return client

    def executeScrypt(self, client, idAction):

        retText = client['temp_logic'].сheckAction(idAction)
        return retText

