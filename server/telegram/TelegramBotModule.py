import telebot
from server.telegram import config
from ai_subsystem.lib.chat import ChatWithModel
from ai_subsystem.lib.config import params_setup
from sys import argv
from tempdlg_subsystem.temp_logic.TempDialogModule import BotDialog

class TelegramBot(object):
    def __init__(self):
        self.AI_activated = False
        #self.startAI()
        self.telebot = telebot.TeleBot(config.token)
        self.installHandlers()
        self.clients = []



    def getAIAnswer(self, question):
        if self.ai_chat:
            return self.ai_chat.GetAnswer(question)[0]
        else:
            return 'Ошибка подсистемы ИИ'

    def getTempAnswer(self, question):
        pass

    def installHandlers(self):
        @self.telebot.message_handler(func=lambda message: True,
                                       content_types=['text'])
        def sendAnswer(message):

            client = self.checkClient(message)
            client = client if client else self.addClient(message)

            if client['ai_activated']:
                self.telebot.send_message(message.chat.id,
                                          self.getAIAnswer(message.text))
            else:
                self.telebot.send_message(message.chat.id,
                                          client['temp_logic'].GetAnswer(
                                              message.text))

    def checkClient(self, message):
        for client in self.clients:
            if message.from_user.id == client['user_id']:
                return client
        return False

    def addClient(self, message):
        self.clients.append({'user_id': message.from_user.id,
                             'first_name' : message.from_user.first_name,
                             'last_name' : message.from_user.last_name,
                             'username' : message.from_user.username,
                             'ai_activated': False,
                             'temp_logic': BotDialog()})
        return self.clients.pop()

    def startAI(self):
       # try:
            if not self.AI_activated:
                self.AI_activated=True
                self.ai_chat = ChatWithModel()
                self.ai_chat.startSession()
        #except:
         #   print('ОШИБКА: не удалось включить модуль ai')
    def startSystem(self):
        self.telebot.polling(none_stop=True)

