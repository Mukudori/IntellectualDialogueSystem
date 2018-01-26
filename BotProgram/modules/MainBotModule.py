from database import DataBaseModule
from database.QuestionTableModule import QuestionTable
from EditDlgForm import EditDlgForm

class MainBot:

    def __init__(self, parent = 0, online=0, voice=0):
        self.Online = online
        self.Voice = voice
        self.tabQ = QuestionTable()
        self.SaveMessage = str()

    def SetOnlineMode(self, mode):
        self.Online = mode
    def SetVoiceMode(self, mode):
        self.Voice = mode

    def ReceiveMessage(self, text):
        if (not len(self.SaveMessage)):
            id = self.tabQ.FindQuestionID(text)
            if (id):
                data = DataBaseModule.GetData(
                    "SELECT answertab.answer, actiontab.id "+
                    "FROM botdb.answertab INNER JOIN (botdb.actiontab INNER JOIN botdb.dlgtab "+
                    "ON actiontab.id = dlgtab.idAction) ON answertab.id = dlgtab.idAnswer "+
                    "WHERE dlgtab.idQuestion ='"+str(id)+"';"
                )
                return data[0]['answer']
            else:
                self.SaveMessage = text
                return "Не понимаю...\nМне запомнить ответ на этот вопрос?"
        else:
            if 'ДА' in text.upper():
                self.EditDlgForm = EditDlgForm(0,self.SaveMessage)
                self.EditDlgForm.show()
                self.SaveMessage = str()
                return 'Хорошо, отрываю форму добавления диалога.'
            else:
                self.SaveMessage = str()
                return 'Вы отказались от добавления диалога.'



