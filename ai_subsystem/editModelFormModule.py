from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout,\
    QListWidgetItem
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import uic
import gzip
import os
import sys
from ai_subsystem import ai

from ai_subsystem.subParser import ParseForm
import threading
import subprocess

class InputForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        workspace = os.path.abspath(os.curdir)+'/ai_subsystem/'
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
        self.carDir = os.path.abspath(os.curdir)+'/ai_subsystem/works/'+modelName
        super(EditModelForm,self).__init__()
        uic.loadUi('ai_subsystem/ui/editAIForm.ui',self)
        self.Model = QStandardItemModel()
        self.Model.setHorizontalHeaderLabels(['Вопрос', 'Ответ'])
        if modelName:
            self.setWindowTitle(modelName)
            self.openDialogs(self.carDir+'/data')
        self.ModeName = modelName
        self.tableView.setModel(self.Model)
        self.AddForm = InputForm(self)
        self.act_Add.triggered.connect(self.add_Click)
        self.act_Del.triggered.connect(self.deleteSelectedRows)
        self.act_Start.triggered.connect(self.saveAndClose)
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

    def deleteSelectedRows(self):
        indices = self.tableView.selectionModel().selectedRows()
        for index in sorted(indices):
            self.Model.removeRow(index.row())

    def saveAndClose(self):
        f_zip = gzip.open("%s/train/chat.txt.gz" % (self.carDir+'/data'), 'w')

        for i in range(self.Model.rowCount()):

            for j in range(2):
                line = (self.Model.item(i, j).text()).encode('UTF-8')
                if '\n'.encode('UTF-8') not in line:
                    line = (self.Model.item(i, j).text() + '\n').encode('UTF-8')

                f_zip.write(line)
        f_zip.close()
#        subprocess.Popen
        self.startTrain()

        self.close()

    def startTrain(self):
        path = sys.argv[0]
        sys.argv.clear()
        sys.argv.append(path)
        sys.argv.append('--mode')
        sys.argv.append('train')
        sys.argv.append('--model_name')
        sys.argv.append(self.ModeName)
       # ai.main(args=sys.argv)

        threading._start_new_thread(ai.main, (sys.argv,))







