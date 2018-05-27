import os
from datetime import datetime

class LogsSaver(object):
    def __init__(self):
        super().__init__()
        self.setupPars()

    def setupPars(self):
        curDir = os.path.abspath(os.curdir)
        endName = datetime.now().strftime("%d.%m.%Y") + ".log"
        allName = 'all_'+endName
        errorName = 'er_'+endName
        self.logsPath = curDir+'/server/logs'
        self.allPath = self.logsPath+'/all/'+allName
        self.answerPath = self.logsPath+'/answer'
        self.errorsPath = self.logsPath+'/errors/'+errorName

    def openFile(self, filePath, mode):
        if 'r' in mode:
            if os.path.exists(filePath):
                f = open(filePath, mode)

            else:
                f = open(filePath,'w')
                f.close()
                f = open(filePath, mode)
        else:
            f = open(filePath,mode)
        return f




    def saveAllLog(self, client, answer, error):
        now_time = datetime.now().strftime("%H:%M:%S")
        text = client['message'].text.replace('\n', '')
        answ = answer.replace('\n', '')
        line = "%s/%s/%s/%s/%s~%s\n" % \
               (now_time, client['idTelegram'],client['username'],
                text, answ, error)
        file = self.openFile(self.allPath, 'a')
        file.write(line)
        file.close()
        if error:
            self.saveErrorLog(client)

    def saveErrorLog(self, client):
        text = client['message'].text.replace('\n', '')
        line = "%s/%s/%s\n" % (client['idClientGroup'], client['username'],
                             text)
        file = self.openFile(self.errorsPath, 'a')
        file.write(line)
        file.close()
