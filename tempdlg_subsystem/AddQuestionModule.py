from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit,QPushButton, \
    QVBoxLayout,QHBoxLayout
from tempdlg_subsystem.database.QuestionTableModule import QuestionTable
from PyQt5.QtGui import QStandardItem
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
            self.Model.setItem(self.INDModel.row(), 1,
                               QStandardItem(self.le.text()))

        self.tv.setModel(self.Model)
        self.close()

    def keyPressEvent(self, event):
        key = event.key()
        if key == 16777220: # код клавиши Enter
            self.click()

    def SetHeaders(self):
        self.label.setText('Введите вопрос :')
        self.setWindowTitle('Ввод вопроса')