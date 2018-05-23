# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox
from tempdlg_subsystem.database.ContextTableModule import ContextTable
from PyQt5.QtGui import QStandardItemModel
from tempdlg_subsystem.database.QuestionTableModule import QuestionTable
from tempdlg_subsystem.database.AnswerTableModule import AnswerTable
from tempdlg_subsystem import ObjectMethodsModule

from tempdlg_subsystem.database.AccessTableModule import AccessTable

from tempdlg_subsystem.AddQuestionModule import AddQuestionDlg
from tempdlg_subsystem.AddAnswerModule import AddAnswerDlg
from tempdlg_subsystem.AddClientsGroupModule import AddGroupDlg


def PrintMessage(title,text, icon =QMessageBox.Critical):
    msg = QMessageBox()
    msg.setIcon(icon)
    # msg.setIconPixmap(pixmap)  # Своя картинка

    msg.setWindowTitle("Ошибка")
    msg.setText(title)
    msg.setInformativeText(text)


    #okButton = msg.addButton('Окей', QMessageBox.AcceptRole)


# Основной класс
class EditContextForm(QWidget):
    def __init__(self, id=0, parent=0, idParent = 0, parentLevel=0):
        super(EditContextForm,self).__init__()
        uic.loadUi('tempdlg_subsystem/ui/ContextEditForm.ui',self)

        self.table = ContextTable()

        self.IDParent = idParent
        if idParent:
            self.ParentLevel = parentLevel+1
            self.ParentForm =parent
        else:
            self.ParentLevel = 0
            self.ParentForm = 0

        if id:
            self.__initEdit(id)
            self.ID = id
        else:
            self.ID = self.table.InsertRecord(header=self.leHeader.text(), idParent=self.IDParent, level=self.ParentLevel)
            self.__initEdit(self.ID)
        if parent:
            self.leHeader.setText(parent.leHeader.text()+" >> ")
            self.leParentContext.setText(parent.leHeader.text())

        self.pbQAdd.clicked.connect(self.AddQuestion)
        self.pbAAdd.clicked.connect(self.AddAnswer)
        self.pbCAdd.clicked.connect(self.AddChildContext)
        self.pbQDel.clicked.connect(self.DeleteSelectedQuestion)
        self.pbADel.clicked.connect(self.DeleteSelectedAnswer)
        self.pbGAdd.clicked.connect(self.AddUserGroup)
        self.pbGDel.clicked.connect(self.DeleteSelectedGroup)
        self.pbSave.clicked.connect(self.SaveContext)
        self.pbQEdit.clicked.connect(self.EditQuestion)
        self.pbAEdit.clicked.connect(self.EditAnswer)
        self.pbCEdit.clicked.connect(self.EditChildContext)

    def RefreshChildContexts(self, id):
        self.modelC = self.table.GetChildContextModelFromParentID(id)
        self.tvChildContext.setModel(self.modelC)


    def __initEdit(self, id):
        try:
            self.Rec = self.table.GetRecordFromID(id)[0]
            if type(self.Rec) == type(list()):
                self.Rec = self.Rec[0]
            self.leHeader.setText(self.table.GetStrFromID(id))
        except:
            PrintMessage('Ошибка контекста', 'Не удалось получить информацию о контексте')

        try:
            self.modelQ= self.table.GetQuestionsModelFromContextID(id)
            self.tvQ.setModel(self.modelQ)
        except:
            PrintMessage('Ошибка вопросов', 'Не удалось получить информацию о вопросах')
            self.modelQ = QStandardItemModel()
        try:
            self.modelA = self.table.GetAnswerModelFromContextID(id)
            self.tvA.setModel(self.modelA)
        except:
            PrintMessage('Ошибка ответов', 'Не удалось получить информацию об ответах')
            self.modelA = QStandardItemModel()
        self.RefreshChildContexts(id)
        self.modelG = self.table.GetGroupsModelFromID(id)
        self.tvG.setModel(self.modelG)
        if self.Rec['idParent']:
            self.leParentContext.setText(self.table.GetStrFromID(self.Rec['idParent']))
        else:
            self.leParentContext.setText("Отсутствует")
        self.ParentLevel = self.Rec['level']

    def AddQuestion(self):
        self.qdlg = AddQuestionDlg(self.tvQ,self.modelQ, self.ID)
        self.qdlg.show()

    def AddAnswer(self):
        self.adlg = AddAnswerDlg(self.tvA,self.modelA, self.ID)
        self.adlg.show()

    def AddChildContext(self):
        if (self.ID):
            self.childConForm = EditContextForm(parent=self, idParent=self.ID)
            self.childConForm.show()


    def DeleteSelectedQuestion(self):
        id,curInd = ObjectMethodsModule.GetSelectedRecordID(self.tvQ)
        QuestionTable().DeleteFromID(id)
        self.modelQ.removeRow(curInd.row())
        self.tvQ.setModel(self.modelQ)

    def DeleteSelectedAnswer(self):
        id, curInd = ObjectMethodsModule.GetSelectedRecordID(self.tvA)
        AnswerTable().DeleteFromID(id)
        self.modelA.removeRow(curInd.row())
        self.tvA.setModel(self.modelQ)

    def AddUserGroup(self):
        self.AUGD = AddGroupDlg(self.tvG, self.modelG, self.ID)
        self.AUGD.show()

    def DeleteSelectedGroup(self):
        id, curInd = ObjectMethodsModule.GetSelectedRecordID(self.tvG)
        AccessTable().DeleteRecordFromContextID(idGroup=id, idContext=self.ID)
        self.modelG.removeRow(curInd.row())
        self.tvG.setModel(self.modelG)

    def SaveContext(self):
        self.table.UpdateRecord(self.ID, self.leHeader.text())
        if self.ParentForm:
            self.ParentForm.RefreshChildContexts(self.IDParent)
        self.close()

    def EditQuestion(self):
        idQ, selInd = ObjectMethodsModule.GetSelectedRecordID(self.tvQ)

        self.qdlg = AddQuestionDlg(self.tvQ, self.modelQ, self.ID, idRecord=idQ, indModel=selInd)
        self.qdlg.show()

    def EditAnswer(self):
        idA, selInd = ObjectMethodsModule.GetSelectedRecordID(self.tvA)
        self.adlg = AddAnswerDlg(tableView=self.tvA,model=self.modelA, idC=self.ID,
                                 idRecord=idA, indModel=selInd)
        self.adlg.show()

    def EditChildContext(self):
        idC, selInd = ObjectMethodsModule.GetSelectedRecordID(self.tvChildContext)

        if selInd:
            self.childConForm = EditContextForm(parent=self,id=idC)
            self.childConForm.show()










