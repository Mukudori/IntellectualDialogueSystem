import os
import pickle
from datetime import datetime
from dbConnector import DataBaseModule as DBM


class WebPageData(object):
    def __init__(self):
        super().__init__()
        self.setupPars()
        self.loadFile()


    def loadFile(self):
        if os.path.exists(self.filePath):
            f = open(self.filePath, "rb")
            self.webList = pickle.load(f)
            f.close()
        else:
            self.rewriteFile()


    def setupPars(self):
        self.webList = [{'id' : 0,
                         'title' : 'Главная страница РИИ',
                         'url' : 'http://rubinst.ru/',
                         'date' : None},]
        self.filePath = os.path.abspath(os.curdir)
        self.filePath+='/tempdlg_subsystem/database/webData.wd'

    def rewriteFile(self):
        self.indexingList()
        with open(self.filePath, 'wb') as f:
            pickle.dump(self.webList, f)


    def getTVModel(self):
        self.indexingList()
        fieldsList = ['id', 'title', 'url', 'date']
        fieldsView = ['id', 'Заголовок', 'Ссылка', 'Дата']
        model = DBM.CreateTableViewModelFromData(data=self.webList,
                                                 fieldTab=fieldsList,
                                                 fieldsView=fieldsView)
        return model

    def indexingList(self):
        for i in range(len(self.webList)):
            self.webList[i]['id']=i

    def insertRecord(self, title, url, date):
        row = {'title' : title,
               'url' : url,
               'date' : date}
        self.webList.append(row)
        self.rewriteFile()

    def deleteRecord(self, id):
        try:
            del self.webList[id]
            self.rewriteFile()
        except:
            print('Ошибка удаления по индексу %s' % id)


