from server.telegram import config
from telebot import TeleBot
from server.telegram.TelegramBotModule import TelegramBot

def Test():
    Bot = TeleBot(config.token)
    #telebot.apihelper.proxy = {'https': 'socks5://195.201.137.246:1080'}


    @Bot.message_handler(func=lambda message: True, content_types=['text'])
    def send_msg(message):
        Bot.send_message(message.chat.id, 'Ваш id : '+str(message.from_user.id))
        Bot.send_message(message.chat.id, 'Имя : '+str(message.from_user.first_name))
        Bot.send_message(message.chat.id, 'Фамилия : '+str(message.from_user.last_name))
        Bot.send_message(message.chat.id, 'user name : '+str(message.from_user.username))
    try:
        Bot.polling(none_stop=True, interval=0)
    except Exception:
        pass

if __name__ == '__main__':
    print("Бот запущен в телеграме")
    #temp_logic = MainTelegramBot()
    #temp_logic.StartTele()
    system = TelegramBot()
    system.startSystem()
