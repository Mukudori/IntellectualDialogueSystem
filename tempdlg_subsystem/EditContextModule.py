# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit,QPushButton, QVBoxLayout,QHBoxLayout,QComboBox, QMessageBox
from tempdlg_subsystem.database.ContextTableModule import ContextTable
from PyQt5.QtGui import QStandardItem
from tempdlg_subsystem.database.QuestionTableModule import QuestionTable
from tempdlg_subsystem.database.AnswerTableModule import AnswerTable
from tempdlg_subsystem import ObjectMethodsModule
from tempdlg_subsystem.database.ActionTableModule import ActionTable
from tempdlg_subsystem.database.AccessTableModule import AccessTable
from tempdlg_subsystem.database.UserGroupModule import UserGroupTable

#Классы для добавления вопросов и ответов
class AddQuestionDlg(QWidget):
    def __init__(self, tableView, model, idC, idRecord=0, indModel=0):
        super().__init__()
        self.IDRecord = idRecord
        self.INDModel = indModel
        self.label = QLabel()
        self.le = QLineEdit()
        self.layH = QHBoxLayout()
        self.layH.addWidget(self.label)
        self.layH.addWidget(self.le)
        self.layV = QVBoxLayout()
        self.layV.addLayout(self.layH)
        self.AddOtherWidgets()
        self.setLayout(self.layV)
        self.tv = tableView
        self.Model = model
        self.IDC = idC

        self.pb.clicked.connect(self.click)
        self.SetHeaders()

    def AddOtherWidgets(self, ):
        self.pb = QPushButton('Добавить')
        self.layV.addWidget(self.pb)
        if self.IDRecord:
            self.le.setText(QuestionTable().GetQuestionFromID(self.IDRecord))


    def click(self):
        tab = QuestionTable()
        if not self.IDRecord:
            id=tab.InsertRecord(self.le.text(), self.IDC)
            i = self.Model.rowCount()

            self.Model.setItem(i,1,QStandardItem(self.le.text()) )
            self.Model.setItem(i,0,QStandardItem(str(id)))
            self.Model.setVerticalHeaderLabels([' '] * (i + 1))
        else:
            tab.UpdateRecordFromIDAndText(self.IDRecord, self.le.text())
            self.Model.setItem(self.INDModel.row(), 1, QStandardItem(self.le.text()))

        self.tv.setModel(self.Model)
        self.close()

    def keyPressEvent(self, event):
        key = event.key()
        if key == 16777220: # код клавиши Enter
            self.click()

    def SetHeaders(self):
        self.label.setText('Введите вопрос :')
        self.setWindowTitle('Ввод вопроса')

class AddAnswerDlg(AddQuestionDlg):
    def AddOtherWidgets(self):
        self.label2 = QLabel('Действие')
        self.layAction =QHBoxLayout()
        self.cb = QComboBox()
        self.layAction.addWidget(self.label2)
        self.layAction.addWidget(self.cb)
        self.pb = QPushButton('Добавить')
        self.layV.addLayout(self.layAction)
        self.layV.addWidget(self.pb)
        self._initComboBox()

        if self.IDRecord:
            answer, action = AnswerTable().GetAnswerAndActionFromAnswerID(self.IDRecord)
            self.le.setText(answer)
            i=0
            for row in self.actTab:
                if row[1] == action:
                    self.cb.setCurrentIndex(i)
                    break
                i+=1
            self.pb.setText('Изменить')


    def SetHeaders(self):
        self.label.setText('Введите ответ на вопрос :')
        self.setWindowTitle('Ввод ответа')

    def _initComboBox(self):
        self.actTab = ActionTable().GetStringAndIDList()
        self.cb.addItems([row[1] for row in self.actTab])

    def click(self):
        text = self.cb.currentText()
        idA = 0
        for row in self.actTab:
            if row[1] == text:
                idA = str(row[0])
                break
        if idA:
            if not self.IDRecord:
                idA =AnswerTable().InsertRecord(self.le.text(),self.IDC, idA)
                i = self.Model.rowCount()
                self.Model.setItem(i, 2, QStandardItem(text))
                self.Model.setItem(i, 1, QStandardItem(self.le.text()))
                self.Model.setItem(i, 0, QStandardItem(str(idA)))
                self.Model.setVerticalHeaderLabels([' '] * (i + 1))

            else:
                AnswerTable().UpdateRecord(id=self.IDRecord ,answer=self.le.text(), idAction = idA)
                i = self.INDModel.row()
                self.Model.setItem(i, 2, QStandardItem(text))
                self.Model.setItem(i, 1, QStandardItem(self.le.text()))
                self.Model.setItem(i, 0, QStandardItem(str(idA)))


        self.tv.setModel(self.Model)
        self.close()

class AddGroupDlg(QWidget):
    def __init__(self, tableView, model, idContext):
        super().__init__()
        self.lay = QVBoxLayout()
        self.cb = QComboBox()
        self.but = QPushButton("Добавить")
        self.lay.addWidget(self.cb)
        self.lay.addWidget(self.but)
        self.setLayout(self.lay)
        self.setWindowTitle("Добавление группы в контекст")

        self.but.clicked.connect(self.click)

        self.tv = tableView
        self.Model = model
        self.idCon = idContext
        self.Groups = UserGroupTable().GetStringAndIDList()
        self.cb.addItems([row[1] for row in self.Groups])
        self.GroupIDList = AccessTable().GetIDGroupListFromIDContext(idContext)

    def click(self):
        idGroup = 0
        for row in self.Groups:
            if row[1] == self.cb.currentText():
                idGroup = row[0]
                break
        if idGroup not in self.GroupIDList:
            AccessTable().AddRecord(idGroup=idGroup, idContext=self.idCon)
            i = self.Model.rowCount()
            self.Model.setItem(i, 1, QStandardItem(self.cb.currentText()))
            self.Model.setItem(i, 0, QStandardItem(str(idGroup)))
            self.Model.setVerticalHeaderLabels([' '] * (i+1))
            self.close()
        else:
            self.qmb = QMessageBox()
            self.qmb.about(self, 'Ошибка', 'Группа пользователей уже имеет доступ к этому контексту.')


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
        self.Rec = self.table.GetRecordFromID(id)[0]
        if type(self.Rec) == type(list()):
            self.Rec = self.Rec[0]
        self.leHeader.setText(self.table.GetStrFromID(id))
        self.modelQ= self.table.GetQuestionsModelFromContextID(id)
        self.tvQ.setModel(self.modelQ)
        self.modelA = self.table.GetAnswerModelFromContextID(id)
        self.tvA.setModel(self.modelA)
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










