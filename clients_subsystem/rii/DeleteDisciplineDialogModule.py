from PyQt5.QtWidgets import QWidget, QVBoxLayout,\
    QHBoxLayout, QLabel, QComboBox, QPushButton

from clients_subsystem.rii.database.TimeTableModule import TimeTable

ClientsGroup = {'Students' : 3, 'Teachers' : 2}

class DeleteDialog(QWidget):
    def __init__(self, idClientsGroup, idClient, numDay, parent=0):
        super().__init__()
        self.idClientsGroup = idClientsGroup
        self.idClient = idClient
        self.numDay = numDay
        self.Parent = parent
        self.initUI()

    def initUI(self):
        vLay = QVBoxLayout()
        hl = QHBoxLayout()
        self.lab = QLabel('Номер пары : ')
        self.cb = QComboBox()
        self.cb.addItems(['1', '2', '3', '4', '5', '6'])
        self.pb = QPushButton('Удалить')
        hl.addWidget(self.lab)
        hl.addWidget(self.cb)

        vLay.addLayout(hl)
        vLay.addWidget(self.pb)

        self.pb.clicked.connect(self.deleteDiscipline)

        self.setLayout(vLay)
        self.setWindowTitle('Удаление пары')

    def getDisciplineList(self):
        if self.idClientsGroup == ClientsGroup['Teachers']:
            return TimeTable().getTeacherList(idTeacher=self.idClient, numDay=self.numDay)
        else:
            return TimeTable().getGroupList(idGroup=self.idClient, numDay=self.numDay)

    def deleteDiscipline(self):
        disList = self.getDisciplineList()
        id=0
        for row in disList:
            if row['numDay'] == self.numDay and row['numLesson']==int(self.cb.currentText()):
                id = row['id']
        TimeTable().deleteDiscipline(id)

        if self.Parent:
            self.Parent.giveTVModel(numDay = self.numDay)

        self.close()





