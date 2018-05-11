## -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListWidgetItem
from PyQt5 import uic
from tempdlg_subsystem.DataBaseForm import DataBaseForm
from tempdlg_subsystem.MessageWidgetModule import MessageWidget
from tempdlg_subsystem.temp_logic.LocalChatModule import LocalChat
from tempdlg_subsystem.SQLForm import SQLForm
from tempdlg_subsystem.SettingFormModule import SettingForm


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi("tempdlg_subsystem/ui/mainwindow.ui", self)
        self.labToolBar = QLabel('<font color=red>Бот не запущен в Telegram<font>')
        self.statusBar.addWidget(self.labToolBar)
        self.PathAdminPic = 'pics/admin.png'
        self.PathBotPic = 'pics/bot.jpg'
        self.LocalBot = LocalChat(self)
        self.EditDlgForm = 0
        self.leMessage.setFocus()
        self.SendMessage('<font color=green size=4><b>Бот</b></font>',
                         self.LocalBot.GetHelloMessage()[0], self.PathBotPic)
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
        answerData = self.LocalBot.ReceiveMessage(AdminMessage)

        self.SendMessage('<font color=blue size=4><b>Админ<b></font>',
                         AdminMessage,self.PathAdminPic)
        self.SendMessage('<font color=green size=4><b>Бот</b></font>',
                         answerData[0]['answer'], self.PathBotPic)
        #potok.start()
        self.leMessage.setText('')
        self.chatWidget.scrollToBottom()
        self.leMessage.setFocus()

        if answerData[0]['executable']:
            answer=self.LocalBot.executeScrypt(idAction=answerData[0]['idAction'],  client=answerData[1])
            self.SendMessage('<font color=green size=4><b>Бот</b></font>',
                             answer, self.PathBotPic)

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
        f = open('tempdlg_subsystem/support.txt','r')
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
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())