# -*- coding: utf-8 -*-
import telebot
from modules.bot import config
from modules.bot.MainBotModule import MainBot


class MainTelegramBot:
    def __init__(self, localBot=0):
        self.GlobalBot = telebot.TeleBot(config.token)
        if localBot :
            self.LocalBot = localBot
        else:
            self.LocalBot = MainBot()
            self.LocalBot.ReConnectToDB()

        @self.GlobalBot.message_handler(func=lambda message: True, content_types=['text'])
        def send_msg(message):
            self.GlobalBot.send_message(message.chat.id, self.LocalBot.GetAnswer(message.text))

        self.Started =1

    def StartTele(self):
        #self.LocalBot.ReConnectToDB()
        self.GlobalBot.polling(none_stop=True)

    def StopTele(self):
        self.GlobalBot.stop_polling()












