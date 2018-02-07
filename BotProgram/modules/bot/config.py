#from telegrambot import bot
token = '412901164:AAFdVoZCHn43QSggrNyD333HWtQ7OzKxXj4'
small_talk_token = '7de17cda70c24186ae02a3d732b02806'


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