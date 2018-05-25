
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
        self.act_Next.setVisible(False)
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
        self.curInd = 1


    def connectSlots(self):
        self.act_Home.triggered.connect(self.goHome)
        self.webView.urlChanged.connect(self.setUrl)
        self.act_Back.triggered.connect(self.backUrl)
        self.pbGo.clicked.connect(self.gotoUrl)
        self.act_Add.triggered.connect(self.saveUrl)
        self.act_Del.triggered.connect(self.delUrl)
        self.act_Browser.triggered.connect(self.openBrowser)
        self.act_Table.triggered.connect(self.openTV)
        self.act_Refresh.triggered.connect(self.refresh)

    def openBrowser(self):
        self.viewBrowser = True
        self.setTableVisible(False)
        self.setBrowserVisible(True)

    def openTV(self):
        self.viewBrowser = False
        self.setTableVisible(True)
        self.setBrowserVisible(False)

    def goHome(self):
        self.webView.load(QUrl(self.HomePage))

    def setUrl(self):
        url = self.webView.url()
        self.leUrl.setText(url.toString())
        self.urlList.append(url)

    def backUrl(self):
        if self.curInd > 0:
            self.curInd -= 1
        if len(self.urlList):
            self.webView.load(self.urlList[self.curInd])

    def nextUrl(self):
        pass

    def gotoUrl(self):
        try:
            url = QUrl(self.leUrl.text())
            self.webView.load(url)
        except:
            print('Произошла ошибка при загрузке страницы')

    def saveUrl(self):
        if self.viewBrowser:
            web = [self.webView.url().toString(), self.webView.title()]
            self.anf = AddNewsForm(web)
        else:
            self.anf = AddNewsForm()
        self.anf.show()

    def refresh(self):
        if self.viewBrowser:
            pass
        else:
            self.tableView.setModel(self.wpData.getTVModel())

    def delUrl(self):
        id = GetSelectedRecordID(self.tableView)[0]
        self.wpData.deleteRecord(id)
        self.tableView.setModel(self.wpData.getTVModel())


