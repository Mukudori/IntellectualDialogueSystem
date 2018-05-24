
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from tempdlg_subsystem.OtherClasses.WebPagesDataModule import WebPageData
from PyQt5.QtCore import QUrl
from tempdlg_subsystem.AddNewsModule import AddNewsForm
from tempdlg_subsystem.ObjectMethodsModule import GetSelectedRecordID

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('tempdlg_subsystem/ui/WebBrowser.ui', self)
        self.setupPars()
        self.connectSlots()

    def setBrowserVisible(self, val):
        self.webView.setVisible(val)
        self.leUrl.setVisible(val)
        self.label.setVisible(val)
        self.act_Back.setVisible(val)
        self.act_Next.setVisible(val)
        self.pbGo.setVisible(val)

    def setTableVisible(self, val):
        self.tableView.setVisible(val)
        self.act_Del.setVisible(val)

    def setupPars(self):
        self.wpData = WebPageData()
        self.tableView.setModel(self.wpData.getTVModel())
        self.HomePage = 'http://rubinst.ru/'
        self.urlList = []
        self.openTV()

    def connectSlots(self):
        self.act_Home.triggered.connect(self.goHome)
        self.webView.urlChanged.connect(self.addUrl)
        self.act_Back.triggered.connect(self.backUrl)
        self.pbGo.clicked.connect(self.gotoUrl)
        self.act_Add.triggered.connect(self.saveUrl)
        self.act_Del.triggered.connect(self.delUrl)
        self.act_Browser.triggered.connect(self.openBrowser)
        self.act_Table.triggered.connect(self.openTV)

    def openBrowser(self):
        self.setTableVisible(False)
        self.setBrowserVisible(True)

    def openTV(self):
        self.setTableVisible(True)
        self.setBrowserVisible(False)

    def goHome(self):
        self.webView.load(QUrl(self.HomePage))

    def addUrl(self):
        self.urlList.append(self.webView.url())

    def backUrl(self):
        if len(self.urlList) == 1:
            shift=1
        else:
            shift=2
        self.webView.load(QUrl(self.urlList[-shift]))

    def gotoUrl(self):
        try:
            url = QUrl(self.leUrl.text())
            self.webView.load(url)
        except:
            print('Произошла ошибка при загрузке страницы')

    def saveUrl(self):
        web = [self.webView.url().toString(), self.webView.title()]
        self.anf = AddNewsForm(web)
        self.anf.show()

    def delUrl(self):
        id = GetSelectedRecordID(self.tableView)[0]
        self.wpData.deleteRecord(id)
        self.tableView.setModel(self.wpData.getTVModel())


