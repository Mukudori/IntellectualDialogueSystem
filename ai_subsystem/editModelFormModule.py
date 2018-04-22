from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout,\
    QListWidgetItem, QDialog, QPushButton
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QColor
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
            item1.setBackground(QColor(200, 100, 100))
            item2 = QStandardItem(self.teA.toPlainText())
            item2.setBackground(QColor(200, 100, 100))
            self.Model.appendRow([item1, item2])
        else:
            self.parseForm = ParseForm(self.Parent)
            self.parseForm.show()
        self.close()

class StartDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.label = QLabel('Вы уверены, что хотите начать обучение? \n\n Процесс обучение требует много времени и ресурсов.')
        self.bY = QPushButton('Да, начать обучение.')
        self.bN = QPushButton('Нет')
        self.vLay = QVBoxLayout()
        self.hLay = QHBoxLayout()
        self.hLay.addWidget(self.bY)
        self.hLay.addWidget(self.bN)
        self.vLay.addWidget(self.label)
        self.vLay.addLayout(self.hLay)
        self.setLayout(self.vLay)
        self.bY.clicked.connect(self.yClick)
        self.bN.clicked.connect(self.nClick)

    def yClick(self):
        self.parent.startTrain()
        self.close()

    def nClick(self):

        self.close()


class EditModelForm(QMainWindow):
    def __init__(self, modelName = 0, parent = 0):
        self.Parent = parent
        self.carDir = os.path.abspath(os.curdir)+'/ai_subsystem/works/'+modelName
        super(EditModelForm,self).__init__()
        uic.loadUi('ai_subsystem/ui/editAIForm.ui',self)
        self.Model = QStandardItemModel()
        if modelName:
            self.setWindowTitle(modelName)
            self.openDialogs(self.carDir+'/data')

        self.ModeName = modelName
        self.tableView.setModel(self.Model)
        self.AddForm = InputForm(self)
        self.act_Add.triggered.connect(self.add_Click)
        self.act_Del.triggered.connect(self.deleteSelectedRows)
        self.act_Start.triggered.connect(self.saveAndStart)
        self.act_Save.triggered.connect(self.save)

    def openDialogs(self, data_dir):
        self.Model.clear()
        self.Model.setHorizontalHeaderLabels(['Вопрос', 'Ответ'])
        f_zip = gzip.open("%s/train/chat.txt.gz" % data_dir, 'r')
        textList =[]
        for line in f_zip:
            lineS = line.decode('UTF-8')
            textList.append(lineS)
        f_zip.close()

        i=0

        while i < len(textList)-1:
            item1 = QStandardItem(str(textList[i]))
            item2 = QStandardItem(str(textList[i+1]))
           # item1.setBackground(QColor(0,0,100))
            self.Model.appendRow([item1,item2])
            i+=2

    def add_Click(self):

        self.AddForm.show()

    def deleteSelectedRows(self):
        indices = self.tableView.selectionModel().selectedRows()
        for index in sorted(indices):
            self.Model.removeRow(index.row())

    def saveAndStart(self):
        self.save()
        self.startDialog = StartDialog(self)
        self.startDialog.exec()

    def save(self):
        f_zip = gzip.open("%s/train/chat.txt.gz" % (self.carDir + '/data'), 'w')
        f_test = open("%s/test/test_set.txt" % (self.carDir + '/data'), 'w')
        for i in range(self.Model.rowCount()):

            for j in range(2):
                line = self.Model.item(i, j).text()
                if '\n' not in line:
                    line += '\n'
                else:
                    line = line.replace('\n', '') + '\n'

                if j == 0:
                    f_test.write(line)
                f_zip.write(line.encode('UTF-8'))
        f_zip.close()
        f_test.close()

        self.openDialogs(self.carDir + '/data')






    def startTrain(self):
        ''' path = sys.argv[0]
        sys.argv.clear()
        sys.argv.append(path)
        sys.argv.append('--mode')
        sys.argv.append('train')
        sys.argv.append('--model_name')
        sys.argv.append(self.ModeName)

       # ai.main(args=sys.argv)

        threading._start_new_thread(ai.main, (sys.argv,))
        #self.Parent.close()'''
        self.Parent.startTraining(self.ModeName)
        self.close()








