#from telegrambot import bot
telebot_token = '412901164:AAFdVoZCHn43QSggrNyD333HWtQ7OzKxXj4'
small_talk_token = 'c16ca22b87e64ee5a5a03c355e5604f5'
token = telebot_token # пока путь по-будет тут, чтобы в классах ничего не поломалось



"""
# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, '''
    Здравствуйте, я ваш персональный помощник. Задавайте свои ответы. ''')
    pass

 # Обработчик для документов и аудиофайлов
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass

 #Обработчик сообщений, подходящих под указанное регулярное выражение
@bot.message_handler(regexp="SOME_REGEXP")
def handle_message(message):
    pass

 # Обработчик сообщений, содержащих документ с mime_type 'text/plain' (обычный текст)
@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def handle_text_doc(message):
    pass
"""