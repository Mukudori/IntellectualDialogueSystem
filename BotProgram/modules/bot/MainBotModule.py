from modules.database import DataBaseModule
from modules.database.QuestionTableModule import QuestionTable
from modules.EditDlgForm import EditDlgForm
from modules.EditActionForm import EditActionForm
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
import os, shutil
import  datetime, time

class MainBot:
    def __init__(self, parent = 0, online=0, voice=0):
        self.Online = online # Бот пишет в телеграме или в программе
        self.Voice = voice # Бот озвучивает свои реплики
        self.ReConnectToDB()
        self.SaveMessage = str() # сообщение, отсутствующее в базе
        self.previousMessage = [str(),0] # Предыдущий ответ бота и его id
        self.UserGroup = 1
        self._mp3_nameold = 'file'
        self.audiodir = 'E:\\Programming\\Python\\IVTAssistant\\BotProgram\\audio\\'
        self.__DelAllAudioFiles() # Чистит папку audio

    def SetOnlineMode(self, mode):
        self.Online = mode
    def SetVoiceMode(self, mode=-1):
        if mode == -1:
            if self.Voice :
                self.Voice = 0
            else:
                self.Voice = 1
        else:
            self.Voice = mode

    def GetHelloMessage(self):
        return ['Здравствуйте!\nЯ ваш персональный помощник.\nРад буду ответить на ваши вопросы.', 0,0]

    def GetAnswer(self, text):
        if (not len(self.SaveMessage)): # Если сообщение отсутствующее в базе пустое
            id = self.tabQ.FindQuestionID(text) # ищем максимально похожий вопрос в базе
            if (id):
                # Если вопрос найден, то получаем ответ на него из базы
                data = DataBaseModule.GetData(
                    "SELECT answertab.answer, dlgtab.idAction, dlgtab.idAnswer "+
                    "FROM botdb.answertab INNER JOIN (botdb.actiontab INNER JOIN botdb.dlgtab "+
                    "ON actiontab.id = dlgtab.idAction) ON answertab.id = dlgtab.idAnswer "+
                    "WHERE dlgtab.idQuestion ='"+str(id)+"';"
                )
                return [data[0]['answer'], data[0]['idAnswer'], data[0]['idAction']]
            else:
                #Иначе запоминаем сообщение и просим его сохранить в базу
                self.SaveMessage = text
                return ["Не понимаю...\nМне запомнить ответ на этот вопрос?", 0,0]
        else:
            if 'ДА' in text.upper():
                #Если пользователь соглашается добавить диалог, то открываем форму
                self.EditDlgForm = EditDlgForm(0,self.SaveMessage)
                self.EditDlgForm.show()
                self.SaveMessage = str()
                return ['Хорошо, отрываю форму добавления диалога.', 0,0]
            else:
                # Иначе игнорируем и стираем вопрос из памяти
                self.SaveMessage = str()
                return ['Вы отказались от добавления диалога.', 0,0]

    def ReceiveMessage(self, text):
        self.previousMessage = self.GetAnswer(text)
        if(self.Voice):
            self.__Say(self.previousMessage[0])
        self.__ExecuteAction(self.previousMessage[2])
        return self.previousMessage[0]

    def __Say(self, phrase):
        # Функция произносит вслух фразу
        mixer.init()
        tts = gTTS(text=phrase, lang="ru")
        now_time = datetime.datetime.now()
        self._mp3_name = now_time.strftime("%d%m%Y%I%M%S") + ".mp3"
        tts.save(self.audiodir+self._mp3_name)
        mixer.music.load(self.audiodir+self._mp3_name)
        mixer.music.play()
        if(os.path.exists(self.audiodir+self._mp3_nameold)):
            os.remove(self.audiodir+self._mp3_nameold)
        now_time = datetime.datetime.now()
        self._mp3_nameold=self._mp3_name
        self._mp3_name = now_time.strftime("%d%m%Y%I%M%S")+".mp3"
        """while True:
            if not mixer.music.get_busy():  # как только воспроизведение музыкального файла закончится
                mixer.quit()  # тогда происходит деактивация модуля mixer
                break  # и выход из программы"""

    def __DelAllAudioFiles(self):
        for the_file in os.listdir(self.audiodir):
            file_path = os.path.join(self.audiodir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    def __ExecuteAction(self, id):
        if (id==13):
            self.f = EditActionForm()
            self.f.show()
        elif(id==14):
            self.f = EditDlgForm()
            self.f.show()

    def ReConnectToDB(self):
        self.tabQ = QuestionTable()  # Список записей из таблицы вопросов








