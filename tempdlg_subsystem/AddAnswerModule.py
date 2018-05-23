from tempdlg_subsystem.AddQuestionModule import AddQuestionDlg
from PyQt5.QtWidgets import  QLabel, QPushButton, \
    QHBoxLayout,QComboBox
from tempdlg_subsystem.database.ActionTableModule import ActionTable
from tempdlg_subsystem.database.AnswerTableModule import AnswerTable
from PyQt5.QtGui import QStandardItem



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
            for row in self.idList:
                if row == action:
                    self.cb.setCurrentIndex(i)
                    break
                i+=1
            self.pb.setText('Изменить')


    def SetHeaders(self):
        self.label.setText('Введите ответ на вопрос :')
        self.setWindowTitle('Ввод ответа')

    def _initComboBox(self):
        actList = ActionTable().GetStringAndIDList()
        self.cb.addItems([row[1] for row in actList])
        self.idList = [row[0] for row in actList]


    def click(self):
        text = self.cb.currentText()
        ci = self.cb.currentIndex()
        idA = self.idList[ci] if self.idList[ci]!=-1 else self.idList[0]

        if idA:
            if not self.IDRecord:
                idA =AnswerTable().InsertRecord( answer=self.le.text(),
                                                idContext=self.IDC,
                                                 idAction=idA)
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