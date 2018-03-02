## -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListWidgetItem
from PyQt5 import uic
from modules.DataBaseForm import  DataBaseForm
from modules.MessageWidgetModule import MessageWidget
from modules.bot.MainBotModule import MainBot
from modules.SQLForm import SQLForm
from modules.SettingFormModule import SettingForm


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("modules/ui/mainwindow.ui", self)
        self.labToolBar = QLabel('<font color=red>Бот не запущен в Telegram<font>')
        self.statusBar.addWidget(self.labToolBar)
        self.PathAdminPic = 'pics/admin.png'
        self.PathBotPic = 'pics/bot.jpg'
        self.LocalBot = MainBot(self)
        self.EditDlgForm = 0
        self.leMessage.setFocus()
        self.SendMessage('<font color=green size=4><b>Бот</b></font>', self.LocalBot.GetHelloMessage()[0], self.PathBotPic)
        self.TeleBotStarted = 0

        self.pbText.clicked.connect(self.SendAdmin)
        self.DB.triggered.connect(self.openDataBaseForm)
        self.checkBox.stateChanged.connect(self.LocalBot.SetVoiceMode)
        self.supportForm.triggered.connect(self.OpenSupport)
        self.action_SQL.triggered.connect(self.OpenSQLForm)
        self.settings.triggered.connect(self.OpenSettingForm)
        self.dbRefresh.triggered.connect(self.LocalBot.ReConnectToDB)
        self.startTele.triggered.connect(self.StartTelegram)


    def changeVoiceMode(self):
        self.Bot.SetVoiceMode()
    def keyPressEvent(self, event):
        key = event.key()
        if key == 16777220: # код клавиши Enter
            self.SendAdmin()

    def openDataBaseForm(self):
        self.f = DataBaseForm()
        self.f.show()

    def SendAdmin(self):
        AdminMessage = self.leMessage.text()
        BotMessage = self.LocalBot.ReceiveMessage(AdminMessage)
        self.SendMessage('<font color=blue size=4><b>Админ<b></font>',AdminMessage,self.PathAdminPic)
        #potok = Thread(target=self.SendMessage, args=('<font color=green size=4><b>Бот</b></font>', BotMessage, self.PathBotPic))
        self.SendMessage('<font color=green size=4><b>Бот</b></font>', BotMessage, self.PathBotPic)
        #potok.start()
        self.leMessage.setText('')
        self.chatWidget.scrollToBottom()
        self.leMessage.setFocus()

    def SendMessage(self, author, text, imgPath):
            # Create QCustomQWidget
        message = MessageWidget()
        message.setTextUp(author)
        message.setTextDown(text)
        message.setIcon(imgPath)
            # Create QListWidgetItem
        myQListWidgetItem = QListWidgetItem(self.chatWidget)
            # Set size hint
        myQListWidgetItem.setSizeHint(message.sizeHint())
            # Add QListWidgetItem into QListWidget
        self.chatWidget.addItem(myQListWidgetItem)
        self.chatWidget.setItemWidget(myQListWidgetItem, message)

    def OpenSupport(self):
        f = open('modules/support.txt','r')
        self.lSupport = QLabel(f.read())
        f.close()
        self.lSupport.setWordWrap(True)
        self.lSupport.setWindowTitle('Справка о программе')
        self.lSupport.show()

    def OpenSQLForm(self):
        self.f = SQLForm(self)
        self.f.show()

    def OpenSettingForm(self):
        self.f = SettingForm()
        self.f.show()

    def StartTelegram(self):
        '''if (not self.TeleBotStarted and 0):
            self.labToolBar.setText('<font color=green>Бот запущен в Telegram<font>')
            self.TeleBot = TelegramBot(self.LocalBot)
            self.TeleBot.start()
            self.TeleBotStarted =1
        else:
            self.labToolBar.setText('<font color=red>Бот не запущен в Telegram<font>')
            self.TeleBot = 0
            self.TeleBotStarted = 0




        #path = os.path.abspath(os.curdir)
        #можно так, но отключат потом только через процессы
        #subprocess.Popen(path+'\\telegrambot\\TelegramBot.py', shell=True)
        #subprocess.call(['xterm', '-e', 'python', path+'\\telegrambot\\TelegramBot.py'])
        '''



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())