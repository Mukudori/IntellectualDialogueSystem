from tempdlg_subsystem.temp_logic.TempDialogModule import TempDialog
from ai_subsystem.lib.chat import ChatWithModel
from main_logic_module.UserMessageModule import UserMessage

class MainDialogLogic(object):
    def __init__(self):
        super().__init__()
        self.clients = []
        self.ai_activated=False
        self.ai_chat=0

    def getAnswerFromMessage(self, message):
        client = self.checkClient(message)
        client = client if client else self.addClient(message)

        if client['ai_activated']:
            return self.ai_chat.GetAnswer(message.text)
        else:
            text=client['temp_logic'].GetAnswer(message.text)
            return text

    def getAnswerFromText(self, text):
        message=UserMessage()
        message.setText(text)
        return self.getAnswerFromMessage(message)

    def addClient(self, message):
        client = dict()
        client['user_id'] = message.from_user.id
        client['first_name'] = message.from_user.first_name
        client['last_name'] = message.from_user.last_name
        client['username'] = message.from_user.username
        client['ai_activated'] = False
        client['temp_logic'] = TempDialog()
        self.clients.append(client)
        return client

    def checkClient(self, message):
        for client in self.clients:
            if message.from_user.id == client['user_id']:
                return client
        return False

    def startAI(self):
       # try:
            if not self.AI_activated:
                self.AI_activated=True
                self.ai_chat = ChatWithModel()
                self.ai_chat.startSession()