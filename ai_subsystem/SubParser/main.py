import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import chardet
from copy import copy
import os
import gzip


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


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

        parseText = QAction(QIcon('open.png'), 'Отфильтровать субтитры', self)
        parseText.triggered.connect(self.parse)

        delDub = QAction(QIcon('open.png'), 'Убрать дублирование', self)
        delDub.triggered.connect(self.deleteDublicates)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Файл')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)

        textMenu = menubar.addMenu('Текст')
        textMenu.addAction(convertText)
        textMenu.addAction(parseText)
        textMenu.addAction(delDub)


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
        while i<len(text):
            line = str()
            f = True
            while f and i<len(text):
                if len(text[i]) > 1:
                    c = ord(text[i][0])
                    f =(c>1039 and c<1107)
                    if f:
                        line+=text[i]+' '
                        i+=1
                else:
                    f=False
            if len(line):
                self.textEdit.append(line)
            i+=1

    def deleteDublicates(self):
        textList = self.textEdit.toPlainText().split('\n')
        i=0
        self.textEdit.clear()
        while i<len(textList):
            self.textEdit.append(textList[i])
            i+=2







if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())