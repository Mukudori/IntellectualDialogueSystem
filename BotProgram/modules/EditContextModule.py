from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QWidget
from modules.database.ContextTableModule import ContextTable

class EditContextForm(QWidget):
    def __init__(self, id=0):
        super().__init__()
        uic.loadUi('modules/ui/ContextEditForm.ui',self)
        self.table = ContextTable()
        if id:
            self.__initEdit(id)


    def __initEdit(self, id):
        self.Rec = self.table.GetRecordFromID(id)
        self.leHeader.setText(self.table.GetStrFromID(id))
        self.modelQ= self.table.GetQuestionsModelFromContextID(id)
        self.tvQ.setModel(self.modelQ)
        self.modelA = self.table.GetAnswerModelFromContextID(id)
        self.tvA.setModel(self.modelA)
        self.modelC = self.table.GetChildContextModelFromParentID(id)
        self.tvChildContext.setModel(self.modelC)
        if self.Rec['idParent']:
            self.leParentContext.setText(self.table.GetStrFromID(self.Rec['idParent']))
        else:
            self.leParentContext.setText("Отсутствует")

