import DataBaseModule
import AnswerTableModule
import QuestionTableModule
import ActionTableModule
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore

class DlgTable:

    def __init__(self):
        self.dlgT = DataBaseModule.GetData('SELECT * FROM dlgtab')
        self.aT = AnswerTableModule.AnswerTable()
        self.qT = QuestionTableModule.QuestionTable()
        self.actT = ActionTableModule.ActionTable()

    def GetItemFromData(self, data):
        pass

    def GetAnswerFromID(self, id):
        pass

    def GetViewModel(self):
        model = QStandardItemModel()
        lenData = len(self.dlgT)
        model.setHorizontalHeaderLabels(['id', 'Вопрос', 'Ответ', 'Действие'])
        model.setVerticalHeaderLabels([' '] * lenData)
        for i in range(lenData):
            item = QStandardItem(str(self.dlgT[i]['id']))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 0, item)

            item = QStandardItem(str(self.qT.GetQuestionFromID(self.dlgT[i]['idQ'])))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 1, item)

            item = QStandardItem(str(self.aT.GetAnswerFromID(self.dlgT[i]['idA'])))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 2, item)

            item = QStandardItem(str(self.actT.GetActionFromID(self.dlgT[i]['idAction'])))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, 3, item)
        return model