from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QPushButton, QDateEdit
from PyQt5.QtCore import QDate
from tempdlg_subsystem.OtherClasses.WebPagesDataModule import WebPageData

class AddNewsForm(QWidget):
    def __init__(self, url=0):
        super().__init__()
        self.initUI()
        self.setupPars(url)
        self.connectSlots()


    def initUI(self):
        vLay = QVBoxLayout()

        h1 = QHBoxLayout()
        self.lab1 = QLabel('Заголовок : ')
        self.leHeader = QLineEdit()
        h1.addWidget(self.lab1)
        h1.addWidget(self.leHeader)
        vLay.addLayout(h1)

        h2 = QHBoxLayout()
        self.lab2 = QLabel('URL : ')
        self.leURL = QLineEdit()
        h2.addWidget(self.lab2)
        h2.addWidget(self.leURL)
        vLay.addLayout(h2)

        h3 = QHBoxLayout()
        self.lab3 = QLabel('Дата : ')
        self.dateEdit = QDateEdit()
        h3.addWidget(self.lab3)
        h3.addWidget(self.dateEdit)
        self.dateEdit.setDate(QDate.currentDate())
        vLay.addLayout(h3)

        self.pbSave = QPushButton('Сохранить')

        vLay.addWidget(self.pbSave)

        self.setWindowTitle('Добавление новости')
        self.setLayout(vLay)

    def getPyDate(self):
        cur_date = self.dateEdit.date()
        return cur_date.toPyDate()

    def setupPars(self, url):
        if url:
            title = url[0]
            if '|' in title:
                title = title.split('|')[0]
            self.leURL.setText(title)
            self.leHeader.setText(url[1])
        self.webData = WebPageData()

    def connectSlots(self):
        self.pbSave.clicked.connect(self.saveRecord)

    def saveRecord(self):
        self.webData.insertRecord(title=self.leHeader.text(),
                                  url=self.leURL.text(),
                                  date=self.getPyDate())
        self.close()





