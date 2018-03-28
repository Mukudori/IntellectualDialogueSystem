# -*- coding: utf-8 -*-
from modules.database import DataBaseModule
from modules.database.QuestionTableModule import QuestionTable
#from modules.EditDlgForm import EditDlgForm
from modules.EditActionForm import EditActionForm
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
import os, shutil
import  datetime, time
from modules.bot.BotDialogModule import BotDialog

class MainBot:
    def __init__(self, parent = 0, online=0, voice=0):
        self.Online = online # Бот пишет в телеграме или в программе
        self.Voice = voice # Бот озвучивает свои реплики
        self.ReConnectToDB()
        self.SaveMessage = str() # сообщение, отсутствующее в базе
        self.previousMessage = [str(),0] # Предыдущий ответ бота и его id
        self.UserGroup = 4
        self._mp3_nameold = 'file'
        self.audioDir=os.path.abspath(os.curdir)+'\\audio\\'
        self.DialogModule = BotDialog(idGroup=self.UserGroup)
        if os.path.exists(self.audioDir):
            self.__DelAllAudioFiles() # Чистит папку audio, если она есть

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

        return self.DialogModule.GetAnswer(text)

    def ReceiveMessage(self, text):
        self.previousMessage = self.GetAnswer(text)
        if(self.Voice):
            self.__Say(self.previousMessage)
        #self.__ExecuteAction(self.previousMessage[2])
        return self.previousMessage

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








