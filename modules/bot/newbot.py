#Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from modules.bot import config
import apiai, json
updater = Updater(token=config.token)
dispatcher = updater.dispatcher

#Обработка комманд
def startCommand(bot, update):
    responce = 'Здравствуйте, я ваш персональный помощник.'
    bot.send_message(chat_id = update.message.chat_id, text=responce)
def textMessage(bot, update):
    request = apiai.ApiAI(config.small_talk_token).text_request()
    request.lang = 'ru'
    #bot.send_message(chat_id=update.message.chat_id, text=responce)
    request.session_id = 'BatlabAIBot' #необходимо чтобы потом обучать бота
    request.query = update.message.text #Посылаем запрос к ИИ с сообщением
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] #Разбираем Json и получаем ответ

    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Не понимаю...')
#Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
#Добавление хендлеров в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)


if __name__ == '__main__':
    #Начинаем поиск обновлений
    updater.start_polling(clean=True)
    #Останавливаем бота при нажатии Ctrl+C
    updater.idle()
