from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout,\
    QListWidgetItem
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import uic
import gzip
import os

from ai_subsystem.subParser import ParseForm

class InputForm(QWidget):
    def __init__(self, parent, workspace):
        super().__init__()
        self.Model = parent.Model
        self.Parent = parent
        uic.loadUi(workspace+'ui/inputMethodForm.ui', self)
        self.textInput = True
        self.setSizeTextEdits(1000,True)
        self.rbFile.clicked.connect(self.sizeHide)
        self.rbInput.clicked.connect(self.sizeShow)
        self.pushButton.clicked.connect(self.AddDialog)



    def setSizeTextEdits(self, h, textinput):
        self.textInput=textinput
        self.label.setMaximumHeight(h)
        self.label_2.setMaximumHeight(h)
        self.teQ.setMaximumHeight(h)
        self.teA.setMaximumHeight(h)

    def sizeHide(self):
        self.setSizeTextEdits(0, False)

    def sizeShow(self):
        self.setSizeTextEdits(1000, True)

    def AddDialog(self):
        if self.textInput:
            item1 = QStandardItem(self.teQ.toPlainText())
            item2 = QStandardItem(self.teA.toPlainText())
            self.Model.appendRow([item1, item2])
        else:
            self.parseForm = ParseForm(self.Parent)
            self.parseForm.show()
        self.close()

class EditModelForm(QMainWindow):
    def __init__(self, modelName = 0):
        self.carDir = os.path.abspath(os.curdir)+'/ai_subsystem/'
        super(EditModelForm,self).__init__()
        uic.loadUi('ai_subsystem/ui/editAIForm.ui',self)
        self.Model = QStandardItemModel()
        self.Model.setHorizontalHeaderLabels(['Вопрос', 'Ответ'])
        if modelName:
            self.setWindowTitle(modelName)
            self.openDialogs(self.carDir+modelName+'works/data')
        self.tableView.setModel(self.Model)
        self.AddForm = InputForm(self, self.carDir)
        self.act_Add.triggered.connect(self.add_Click)

    def openDialogs(self, data_dir):
        f_zip = gzip.open("%s/train/chat.txt.gz" % data_dir, 'r')
        textList =[]
        for line in f_zip:
            textList.append(line)
        f_zip.close()

        i=0

        while i < len(textList)-1:
            item1 = QStandardItem(str(textList[i].decode('UTF-8')))
            item2 = QStandardItem(str(textList[i+1].decode('UTF-8')))
            self.Model.appendRow([item1,item2])
            i+=2

    def add_Click(self):

        self.AddForm.show()


