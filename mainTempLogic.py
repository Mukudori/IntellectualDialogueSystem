## -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListWidgetItem
from PyQt5 import uic
from tempdlg_subsystem.DataBaseForm import DataBaseForm
from tempdlg_subsystem.MessageWidgetModule import MessageWidget
from tempdlg_subsystem.temp_logic.LocalChatModule import LocalChat
from tempdlg_subsystem.SQLForm import SQLForm
from tempdlg_subsystem.SettingFormModule import SettingForm
# Клиентские подсистемы
from clients_subsystem.rii.database.CathedraModule import Cathedra
from clients_subsystem.rii.database.ClientModule import Client
from clients_subsystem.rii.database.CathGroupModule import CathGroup


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi("tempdlg_subsystem/ui/mainwindow.ui", self)
        self.initUI()
        self.setupPars()
        self.LocalBot = LocalChat(parent=self)
        self.connectSlots()

        self.SendMessage('<font color=green size=4><b>Бот</b></font>',
                         self.LocalBot.GetHelloMessage()[0], self.PathBotPic)


    def initUI(self):
        self.labToolBar = QLabel('<font color=red>Локальный режим системы<font>')
        self.statusBar.addWidget(self.labToolBar)
        self.leMessage.setFocus()
        self.setVisibleOtherCB(False)


    def connectSlots(self):
        self.pbText.clicked.connect(self.SendAdmin)
        self.DB.triggered.connect(self.openDataBaseForm)
        self.checkBox.stateChanged.connect(self.LocalBot.SetVoiceMode)
        self.supportForm.triggered.connect(self.OpenSupport)
        self.action_SQL.triggered.connect(self.OpenSQLForm)
        self.settings.triggered.connect(self.OpenSettingForm)
        self.dbRefresh.triggered.connect(self.LocalBot.ReConnectToDB)
        self.cbClient.currentIndexChanged.connect(self.setupOtherCB)
        self.cbCath.currentIndexChanged.connect(self.refreshOtherCB)

    def setupPars(self):
        self.PathAdminPic = 'pics/admin.png'
        self.PathBotPic = 'pics/bot.jpg'
        self.EditDlgForm = 0
        self.cathList = 0 # Список кафедр
        self.groupList = 0 # Список групп студентов
        self.teachersList = 0 # Список преподавателей



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

    def setVisibleOtherCB(self, val):
        self.lOther.setVisible(val)
        self.cbOther.setVisible(val)
        self.lCath.setVisible(val)
        self.cbCath.setVisible(val)

    def refreshOtherCB(self):
        ind = self.cbCath.currentIndex()
        if ind == -1:
            ind = self.cathList[0]['id']
        else:
            ind=self.cathList[ind]['id']


        curText = self.cbClient.currentText()
        if curText == 'Преподаватель':
            self.initTeachers(idCath=ind)
        else:
            self.initGroup(idCath=ind)

    def initCath(self):
        self.cathList = Cathedra().getList()
        self.cbCath.clear()
        self.cbCath.addItems([row['name'] for row in self.cathList])

    def initTeachers(self, idCath=0):
        if not idCath:
            self.initCath()
            idCath=1
        self.teachersList = Client().getTeachersListFromIDCath(idCath=idCath)
        self.cbOther.clear()
        self.cbOther.addItems([row['shortfio'] for row in self.teachersList])

    def initGroup(self, idCath=0):
        if not idCath:
            self.initCath()
            idCath=1
        self.groupList = CathGroup().getList(idCath=idCath)
        self.cbOther.clear()
        self.cbOther.addItems([row['name'] for row in self.groupList])

    def setupOtherCB(self):

        def _setVis(val):
            self.setVisibleOtherCB(val)

        curText = self.cbClient.currentText()

        if curText == 'Администратор':
            _setVis(False)
        elif curText == 'Преподаватель':
            _setVis(True)
            self.initTeachers()
        elif curText == 'Студент':
            _setVis(True)
            self.initGroup()
        elif curText == 'Гость':
            _setVis(False)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())