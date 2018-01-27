## -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListWidgetItem
from PyQt5 import uic, QtCore
from DataBaseForm import  DataBaseForm
from MessageWidgetModule import MessageWidget
from MainBotModule import MainBot


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/mainwindow.ui", self)
        self.labToolBar = QLabel('<font color=red>Бот не запущен в Telegram<font>')
        self.statusBar.addWidget(self.labToolBar)
        self.DB.triggered.connect(self.openDataBaseForm)
        self.PathAdminPic = '../pics/admin.png'
        self.PathBotPic = '../pics/bot.jpg'
        self.Bot = MainBot(self)
        self.EditDlgForm = 0
        self.leMessage.setFocus()
        self.SendMessage('<font color=green size=4><b>Бот</b></font>', self.Bot.GetHelloMessage()[0], self.PathBotPic)


        self.pbText.clicked.connect(self.SendAdmin)
        self.checkBox.stateChanged.connect(self.changeVoiceMode)

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
        BotMessage = self.Bot.ReceiveMessage(AdminMessage)
        self.SendMessage('<font color=blue size=4><b>Админ<b></font>',AdminMessage,self.PathAdminPic)
        self.SendMessage('<font color=green size=4><b>Бот</b></font>', BotMessage, self.PathBotPic)
        self.leMessage.setText('')
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




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())