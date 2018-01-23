from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from database import ActionTableModule
from database.DlgTableModule import DlgTable


class EditDlgForm(QWidget):

    def __init__(self, id):
        super().__init__()
        uic.loadUi("ui/EditDlgForm.ui", self)
        self.ActTab = ActionTableModule.ActionTable()
        self.comboBox.addItems(self.ActTab.GetList())
        self.rbCreateNew.toggled.connect(self.triggerNew)
        self.rbFromList.toggled.connect(self.triggerList)
        self.ID = id
        if (id):
            self.setWindowTitle('Редактирование диалога #'+str(id))
            listRec = DlgTable().GetDialogListFromID(id)
            self.teQ.clear()
            self.teQ.append(listRec[0])
            self.teA.clear()
            self.teA.append(listRec[1])
            i=0
            for i in range(self.comboBox.count()):
                if self.comboBox.itemText(i) == listRec[2]:
                    self.comboBox.setCurrentIndex(i)
        else:
            self.setWindowTitle('Добавление нового диалога')


    def triggerNew(self):
        self.comboBox.setMaximumHeight(0)
    def triggerList(self):
        self.comboBox.setMaximumHeight(20)
