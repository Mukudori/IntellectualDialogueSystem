from database.ActionTableModule import ActionTable
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QWidget

class EditActionForm(QWidget):
    def __init__(self, id=0, parent=0):
        super().__init__()
        uic.loadUi('ui/EditActionForm.ui',self)
        self.ID=int(id)
        if(id):
            self.table = ActionTable()
            rec = self.table.GetDataFromID(self.ID)
            self.leAction.setText(rec['action'])
            self.teComand.setText(rec['command'])
            self.teNote.setText(rec['note'])
            self.pbSave.clicked.connect(self.UpdateRecord)
        else:
            self.pbSave.clicked.connect(self.InsertRecord)

    def InsertRecord(self):
        table = ActionTable()
        table.InsertRecord(self.leAction.text(),
                           self.teComand.toPlainText(),
                           self.teNote.toPlainText())
        self.close()

    def UpdateRecord(self):
        table = ActionTable()
        table.UpdateRecord(self.ID,
                           self.leAction.text(),
                           self.teComand.toPlainText(),
                           self.teNote.toPlainText())
        self.close()

    def DeleteRecord(self,id):
        pass

