## -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListWidgetItem
from PyQt5 import uic
from DataBaseForm import  DataBaseForm
from MessageWidgetModule import MessageWidget
from PyQt5 import QtGui

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/mainwindow.ui", self)
        self.labToolBar = QLabel('<font color=red>Бот не запущен в Telegram<font>')
        self.statusBar.addWidget(self.labToolBar)
        self.DB.triggered.connect(self.openDataBaseForm)
        self.PathAdminPic = '../pics/admin.png'
        self.PathBotPic = '../pics/bot.png'
        self.pbText.clicked.connect(self.SendAdmin)

    def openDataBaseForm(self):
        self.f = DataBaseForm()
        self.f.show()

    def SendAdmin(self):
        self.SendMessage('Админ',self.leMessage.text(),self.PathAdminPic)

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