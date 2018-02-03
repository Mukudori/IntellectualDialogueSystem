from modules.database import QuestionTableModule, DataBaseModule, ActionTableModule, AnswerTableModule
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore
from modules.database.QuestionTableModule import QuestionTable
#from modules.database.ActionTableModule import ActionTable
from modules.database.AnswerTableModule import AnswerTable


class DlgTable:

    def __init__(self):
        self.dlgT = DataBaseModule.GetData('SELECT * FROM dlgtab')

    def __ConnectToAllTables(self):

        self.aT = AnswerTableModule.AnswerTable()
        self.qT = QuestionTableModule.QuestionTable()
        self.actT = ActionTableModule.ActionTable()

    def __ConnectToQuestion(self):
        self.qT = QuestionTableModule.QuestionTable()

    def __ConnectToAnswer(self):
        self.aT = AnswerTableModule.AnswerTable()

    def __ConnectToAction(self):
        self.actT = ActionTableModule.ActionTable()

    def GetRecordFromID(self, id):
        for record in self.dlgT:
            if record['id'] == id:
                return record
        return {'id': 0 , 'idQuestion' : 0, 'idAnswer' : 0, 'idAction' : 0}

    def GetDialogListFromID(self,id):
        self.__ConnectToAllTables()
        rec = self.GetRecordFromID(id)
        return [self.qT.GetQuestionFromID(rec['idQuestion']),
                self.aT.GetAnswerFromID(rec['idAnswer']),
                self.actT.GetActionFromID(rec['idAction'])]

    def GetViewModel(self):
        self.__ConnectToAllTables()
        model = QStandardItemModel()
        lenData = len(self.dlgT)
        model.setHorizontalHeaderLabels(['id', 'Вопрос', 'Ответ', 'Действие'])
        model.setVerticalHeaderLabels([' '] * lenData)

        for i in range(lenData):
            item = QStandardItem(str(self.dlgT[i]['id']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 0, item)

            item = QStandardItem(str(self.qT.GetQuestionFromID(self.dlgT[i]['idQuestion'])))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 1, item)

            item = QStandardItem(str(self.aT.GetAnswerFromID(self.dlgT[i]['idAnswer'])))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 2, item)

            item = QStandardItem(str(self.actT.GetActionFromID(self.dlgT[i]['idAction'])))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 3, item)
        return model

    def InsertRecord(self, question, answer, actionID):
        self.__ConnectToAllTables()
        idQuestion = self.qT.InsertRecord(question)
        idAnswer = self.aT.InsertRecord(answer)
        currentid = DataBaseModule.ExecuteSQL('''
        INSERT INTO dlgtab (idQuestion,idAnswer,idAction) 
         VALUES (\'''' + str(idQuestion)+"','"+str(idAnswer)+"','"+str(actionID)+"');")
        return currentid

    def DeleteRecord(self, id):
        rec = self.GetRecordFromID(id)
        idQuestion = rec['idQuestion']
        idAnswer = rec['idAnswer']
        idDlg = rec['id']
        DataBaseModule.ExecuteSQL(
            "DELETE FROM questiontab WHERE id='"+str(idQuestion)+"'; "+
            "DELETE FROM answertab WHERE id='"+str(idAnswer)+"'; "+
            "DELETE FROM dlgtab WHERE id='"+str(idDlg)+"';")

    def UpdateRecord(self, idDlg, question, answer, actionID):
        rec = self.GetRecordFromID(idDlg)
        QuestionTable().UpdateRecordFromIDAndText(rec['idQuestion'], question)
        AnswerTable().UpdateRecordFromIDAndText(rec['idAnswer'],answer)

        if (actionID != rec['idAction']):
            DataBaseModule.ExecuteSQL(
                "UPDATE dlgtab "+
                "SET idAction='"+str(actionID)+"' "
                "WHERE id ='"+str(idDlg)+"';"
            )
