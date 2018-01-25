from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from database import ActionTableModule
from database.DlgTableModule import DlgTable
from database.ActionTableModule import ActionTable


class EditDlgForm(QWidget):

    def __init__(self, id=0, text=''):
        super().__init__()
        uic.loadUi("ui/EditDlgForm.ui", self)
        self.ActTab = ActionTableModule.ActionTable()
        self.comboBox.addItems(self.ActTab.GetList())
        self.rbCreateNew.toggled.connect(self.triggerNew)
        self.rbFromList.toggled.connect(self.triggerList)
        self.ID = id
        self.NewAct = 0
        if (id):
            self.initEdit()
        else:
            if len(text):
                self.teQuestion.append(text)
            else:
                self.initCreate()


    def triggerNew(self):
        self.comboBox.setMaximumHeight(0)
        self.gbAction.setMaximumHeight(300)
        self.ActTab = 1
    def triggerList(self):
        self.comboBox.setMaximumHeight(20)
        self.gbAction.setMaximumHeight(0)
        self.ActTab = 0

    def initEdit(self):
        self.setWindowTitle('Редактирование диалога #' + str(self.ID))
        listRec = DlgTable().GetDialogListFromID(self.ID)
        self.teQ.clear()
        self.teQ.append(listRec[0])
        self.teA.clear()
        self.teA.append(listRec[1])
        i = 0
        for i in range(self.comboBox.count()):
            if self.comboBox.itemText(i) == listRec[2]:
                self.comboBox.setCurrentIndex(i)
        self.pbSave.clicked.connect(self.__EditRecord)

    def initCreate(self):
        self.setWindowTitle('Добавление нового диалога')
        self.pbSave.clicked.connect(self.__CreateRecord)

    def __CreateRecord(self):
        id = self.__CreateAction()
        if (id):
            DlgTable().InsertRecord(
                self.teQ.toPlainText(),
                self.teA.toPlainText(),
                id
            )
        else:
            DlgTable().InsertRecord(
                self.teQ.toPlainText(),
                self.teA.toPlainText(),
                ActionTable().GetIDFromActionStr(self.comboBox.currentText())
            )
        self.close()

    def __EditRecord(self):
        id = self.__CreateAction()
        if (id):
            DlgTable().UpdateRecord(
                self.ID,
                self.teQ.toPlainText(),
                self.teA.toPlainText(),
                id
            )
        else:
            DlgTable().UpdateRecord(
                self.ID,
                self.teQ.toPlainText(),
                self.teA.toPlainText(),
                ActionTable().GetIDFromActionStr(self.comboBox.currentText())
            )

        self.close()

    def __CreateAction(self):
        if self.NewAct:
            return ActionTable().InsertRecord(
                self.leAction.text(),
                self.teComand.toPlainText(),
                self.teNote.toPlainText()
            )
        else:
            return 0