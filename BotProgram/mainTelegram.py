from modules.bot.TelegramBot import MainTelegramBot
import telebot
from modules.bot import config

def Test():
    Bot = telebot.TeleBot(config.token)

    @Bot.message_handler(func=lambda message: True, content_types=['text'])
    def send_msg(message):
        Bot.send_message(message.chat.id, 'Ваш id : '+str(message.from_user.id))
        Bot.send_message(message.chat.id, 'Имя : '+str(message.from_user.first_name))
        Bot.send_message(message.chat.id, 'Фамилия : '+str(message.from_user.last_name))
        Bot.send_message(message.chat.id, 'user name : '+str(message.from_user.username))
    Bot.polling(none_stop=True)

if __name__ == '__main__':
    print("Бот запущен в телеграме")
    #bot = MainTelegramBot()
    #bot.StartTele()
    Test()
