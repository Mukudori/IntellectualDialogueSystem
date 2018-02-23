from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit,QPushButton, QVBoxLayout,QHBoxLayout,QComboBox, QMessageBox
from modules.database.ContextTableModule import ContextTable
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from modules.database.QuestionTableModule import QuestionTable
from modules.database.AnswerTableModule import AnswerTable
from modules import ObjectMethodsModule
from modules.database.ActionTableModule import ActionTable
from modules.database.AccessTableModule import AccessTable
from modules.database.UserGroupModule import UserGroupTable

#Классы для добавления вопросов и ответов
class AddQuestionDlg(QWidget):
    def __init__(self, tableView, model, idC):
        super().__init__()
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

    def AddOtherWidgets(self):
        self.pb = QPushButton('Добавить')
        self.layV.addWidget(self.pb)

    def click(self):
        tab = QuestionTable()
        id=tab.InsertRecord(self.le.text(), self.IDC)
        i = self.Model.rowCount()

        self.Model.setItem(i,1,QStandardItem(self.le.text()) )
        self.Model.setItem(i,0,QStandardItem(str(id)))
        self.tv.setModel(self.Model)
        self.close()

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

    def SetHeaders(self):
        self.label.setText('Введите ответ на вопрос :')
        self.setWindowTitle('Ввод ответа')

    def _initComboBox(self):
        self.actTab = ActionTable().GetStringAndIDList()
        self.cb.addItems([row[1] for row in self.actTab])

    def click(self):
        text = self.cb.currentText()
        id = 0
        for row in self.actTab:
            if row[1] == text:
                id = str(row[0])
                break
        if id:
            idA =AnswerTable().InsertRecord(self.le.text(),self.IDC)
            i = self.Model.rowCount()
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
        super().__init__()
        uic.loadUi('modules/ui/ContextEditForm.ui',self)

        self.table = ContextTable()

        self.IDParent = idParent
        if idParent:
            self.ParentLevel = parentLevel+1

        if id:
            self.__initEdit(id)
            self.ID = id
        else:
            self.ID = self.table.InsertRecord(header=self.leHeader.text(), idParent=self.IDParent, level=self.ParentLevel)
            self.__initEdit(id)
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



    def __initEdit(self, id):
        self.Rec = self.table.GetRecordFromID(id)
        self.leHeader.setText(self.table.GetStrFromID(id))
        self.modelQ= self.table.GetQuestionsModelFromContextID(id)
        self.tvQ.setModel(self.modelQ)
        self.modelA = self.table.GetAnswerModelFromContextID(id)
        self.tvA.setModel(self.modelA)
        self.modelC = self.table.GetChildContextModelFromParentID(id)
        self.tvChildContext.setModel(self.modelC)
        self.modelG = self.table.GetGroupsModelFromID(id)
        self.tvG.setModel(self.modelG)
        if self.Rec['idParent']:
            self.leParentContext.setText(self.table.GetStrFromID(self.Rec['idParent']))
        else:
            self.leParentContext.setText("Отсутствует")

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
        self.close()





