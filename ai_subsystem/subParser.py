import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QMessageBox)
from PyQt5.QtGui import QIcon, QStandardItem,QColor
import chardet
from copy import copy
import os
import gzip


class ParseForm(QMainWindow):

    def __init__(self, parent=0):
        super().__init__()

        self.initUI()

        if parent:
            self.Model = parent.Model
        else:
            self.Model = 0



    def initUI(self):

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Открыть', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Открыть файл')
        openFile.triggered.connect(self.showDialog)

        saveFile = QAction(QIcon('open.png'), 'Сохранить (/result/chat*.txt)', self)
        saveFile.triggered.connect(self.save)

        convertText=QAction(QIcon('open.png'), 'Вернуть первоначальный вид', self)
        convertText.triggered.connect(self.backStartText)

        parseText = QAction(QIcon('open.png'), 'Отфильтровать субтитры и привести в нужный формат', self)
        parseText.triggered.connect(self.parse)

        delDub = QAction(QIcon('open.png'), 'Убрать дублирование', self)
        delDub.triggered.connect(self.deleteDublicates)

        Add = QAction(QIcon('open.png'), 'Добавить диалоги в модель', self)
        Add.triggered.connect(self.AddData)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Файл')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)

        textMenu = menubar.addMenu('Текст')
        textMenu.addAction(convertText)
        textMenu.addAction(parseText)
        textMenu.addAction(delDub)
        textMenu.addAction(Add)


        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Парсер субтитров')
        self.show()
        self.Text = str()


    def showDialog(self):

        def converter(filePath):
            if any([filePath.endswith(extension) for extension in '.srt,.ass,.txt'.split(',')]):
                with open(filePath, "rb") as F:
                    text = F.read()
                    enc = chardet.detect(text).get("encoding")
                    if enc and enc.lower() != "utf-8":
                        try:
                            text = text.decode(enc)
                            self.statusBar().showMessage('Сконвернировано в UTF-8')
                            return text.encode("utf-8").decode("utf-8")
                        except:
                            return u"Ошибка в имени файла: название содержит русские символы."
                    else:
                        self.statusBar().showMessage(
                            u"Файл находится в кодировке %s и не требует конвертирования." % enc)

                        return text.decode("utf-8")
        fname = QFileDialog.getOpenFileName(self, 'Открыть файл', '/home')[0]

        self.Text = converter(fname)
        self.textEdit.clear()

        self.textEdit.append(self.Text)

    def save(self):
        resultDir = os.curdir+'/result'

        ldir = [ nfile for nfile in os.listdir(resultDir)
                 if 'chat' in nfile]
        i=1
        if len(ldir):
            name = 'chat.txt'
            while True:
                if name not in ldir:
                    f = open(resultDir+'/'+name,'w')
                    text = self.textEdit.toPlainText()
                    f.write(text)
                    f.close()
                    break
                else:
                    name = 'chat'+str(i)+'.txt'
                    i+=1
        else:
            f = open(resultDir + '/chat.txt', 'w')
            f.write(self.textEdit.toPlainText())
            f.close()

    def backStartText(self):
        self.textEdit.clear()
        self.textEdit.setText(self.Text)

    def parse(self):
        text = copy(self.Text).split('\r\n')
        self.textEdit.clear()
        i=0
        j=0
        line=str()
        while i<len(text):
            buf = str()
            f = True
            while f and i<len(text):
                if len(text[i]) > 1:
                    c = ord(text[i][0])
                    f =(c>1039 and c<1107)
                    if f:
                        buf+=text[i].replace('\n', '')+' '
                        i+=1
                else:
                    f=False
            if len(buf):

                if j==1:
                    line+=' => '+buf
                    self.textEdit.append(line)
                    j=0
                else:
                    line=buf
                    j=1
            i+=1

    def deleteDublicates(self):
        textList = self.textEdit.toPlainText().split('\n')
        i=0
        self.textEdit.clear()
        while i<len(textList):
            self.textEdit.append(textList[i])
            i+=2

    def AddData(self):
        text = self.textEdit.toPlainText().split('\n')
        try:
            for line in text:
                q,a = line.split('=>')
                item1 = QStandardItem(q)
                item1.setBackground(QColor(200, 100, 100))
                item2 = QStandardItem(a)
                item2.setBackground(QColor(200, 100, 100))
                self.Model.appendRow([item1, item2])
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Ошибка")
            msg.setInformativeText("Диалоги имеют не тот формат")
            msg.setWindowTitle("Ошибка")
            msg.show()



