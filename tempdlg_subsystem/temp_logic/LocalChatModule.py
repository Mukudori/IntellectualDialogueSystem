# -*- coding: utf-8 -*-
from tempdlg_subsystem.database.QuestionTableModule import QuestionTable
from gtts import gTTS
from pygame import mixer
import os
import  datetime
from main_logic_module.MainDialogLogicModule import MainDialogLogic

class LocalChat:
    def __init__(self, parent = 0, voice=0):
        self.setupPars(voice)

        self.ReConnectToDB()

        self.LogicModule = MainDialogLogic()

    def setupPars(self, voice=0):
        self.Voice = voice  # Бот озвучивает свои реплики
        self.SaveMessage = str()  # сообщение, отсутствующее в базе
        self.previousMessage = [str(), 0]  # Предыдущий ответ бота и его id
        self.UserGroup = 4
        self._mp3_nameold = 'file'
        self.audioDir = os.path.abspath(os.curdir) + '//audio//' # Установки папки с аудио
        if os.path.exists(self.audioDir):
            self.__DelAllAudioFiles() # Чистит папку audio, если она есть


    def SetVoiceMode(self, mode=-1):
        if mode == -1:
            if self.Voice :
                self.Voice = 0
            else:
                self.Voice = 1
        else:
            self.Voice = mode

    def GetHelloMessage(self):
        return ['Здравствуйте!\nЯ далоговая система.\nРада буду ответить на ваши вопросы.', 0,0]

    def GetAnswer(self, text):
        return self.LogicModule.getAnswerFromText(text)

    def ReceiveMessageFromText(self, text):
        self.previousMessage = self.GetAnswer(text)
        textAnswer = self.previousMessage['answerData']['answer']
        if(self.Voice):
            self.__Say(textAnswer)
        return self.previousMessage

    def ReceiveMessageFromUserMessage(self, message):
        self.previousMessage = self.LogicModule.getAnswerFromMessage(message)
        textAnswer = self.previousMessage['answerData']['answer']
        if (self.Voice):
            self.__Say(textAnswer)

        return self.previousMessage

    def executeScrypt(self, client, idAction):
        textAnswer = self.LogicModule.executeScrypt(idAction=idAction, client=client)
        if (self.Voice):
            self.__Say(textAnswer)
        return textAnswer

    def __Say(self, phrase):
        # Функция произносит вслух фразу
        mixer.init()
        tts = gTTS(text=phrase, lang="ru")
        now_time = datetime.datetime.now()
        self._mp3_name = now_time.strftime("%d%m%Y%I%M%S") + ".mp3"
        tts.save(self.audioDir+self._mp3_name)
        mixer.music.load(self.audioDir+self._mp3_name)
        mixer.music.play()
        #if(os.path.exists(self.audioDir+self._mp3_nameold)):
           # os.remove(self.audioDir+self._mp3_nameold)
        now_time = datetime.datetime.now()
        self._mp3_nameold=self._mp3_name
        self._mp3_name = now_time.strftime("%d%m%Y%I%M%S")+".mp3"
        while True:
            if not mixer.music.get_busy():  # как только воспроизведение музыкального файла закончится
                mixer.quit()  # тогда происходит деактивация модуля mixer
                break  # и выход из программы"""

    def __DelAllAudioFiles(self):
        for the_file in os.listdir(self.audioDir):
            file_path = os.path.join(self.audioDir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    def ReConnectToDB(self):
        self.tabQ = QuestionTable()  # Список записей из таблицы вопросов









