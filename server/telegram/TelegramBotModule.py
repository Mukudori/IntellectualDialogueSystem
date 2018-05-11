import telebot
from server.telegram import config
from main_logic_module.MainDialogLogicModule import MainDialogLogic

class TelegramBot(object):
    def __init__(self):
        self.AI_activated = False
        #self.startAI()
        self.telebot = telebot.TeleBot(config.token)
        self.installHandlers()
        self.clients = []
        self.mainLogicModule = MainDialogLogic()



    def getAnswer(self, message):
        answerData = self.mainLogicModule.getAnswerFromMessage(message)
        return answerData



    def installHandlers(self):
        @self.telebot.message_handler(func=lambda message: True,
                                       content_types=['text'])
        def sendAnswer(message):
            ansDat = self.getAnswer(message)

            self.telebot.send_message(message.chat.id,
                                         ansDat[0]['answer'])
            if ansDat[0]['executable']:
                ansDat = self.mainLogicModule.executeScrypt(
                    client=ansDat[1], idAction=ansDat['idAction'])
                self.telebot.send_message(message.chat.id,
                                          ansDat[0]['answer'])



    def startSystem(self):
        self.telebot.polling(none_stop=True)

