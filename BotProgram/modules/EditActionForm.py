from modules.database.ActionTableModule import ActionTable
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QWidget


class EditActionForm(QWidget):
    def __init__(self, id=0, parent=0):
        super().__init__()
        uic.loadUi('modules/ui/EditActionForm.ui',self)
        self.ID=int(id)
        self.check = False
        if(id):
            self.table = ActionTable()
            rec = self.table.GetDataFromID(self.ID)
            self.leAction.setText(rec['action'])

            try:
                f = open('modules/bot/scrypts/id_'+ str(rec['id'])+'.py', 'r', encoding='utf-8')

                self.teScrypt.setText(f.read())
                self.groupBox.setMaximumHeight(16777215)
                self.check = True
            except:
                self.check = False
                self.teScrypt.setText('Скрипт отсутствует')
                self.groupBox.setMaximumHeight(0)

            self.teNote.setText(rec['note'])
            self.pbSave.clicked.connect(self.UpdateRecord)
        else:
            self.pbSave.clicked.connect(self.InsertRecord)

        self.checkBox.setChecked(self.check)
        self.checkBox.stateChanged.connect(self.CheckScrypt)

    def InsertRecord(self):
        table = ActionTable()
        self.ID=table.InsertRecord(  self.leAction.text(),
                           self.teNote.toPlainText(),
                           1 if self.check else 0)
        if self.check:
            f = open('modules/bot/scrypts/id_' + str(self.ID) + '.py', 'w', encoding='utf-8')
            f.write(self.teScrypt.toPlainText())
            f.close()
        self.close()

    def UpdateRecord(self):
        table = ActionTable()
        table.UpdateRecord(self.ID,
                           self.leAction.text(),
                           self.teNote.toPlainText(),
                           1 if self.check else 0)
        if self.check:
            f = open('modules/bot/scrypts/id_' + str(self.ID) + '.py', 'w', encoding='utf-8')
            f.write(self.teScrypt.toPlainText())
            f.close()
        self.close()

    def CheckScrypt(self):
        if self.check:
            self.check=False
            self.teScrypt.clear()
            self.groupBox.setMaximumHeight(0)

        else:
            self.check=True
            self.groupBox.setMaximumHeight(16777215)

