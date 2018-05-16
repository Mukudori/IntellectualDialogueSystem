from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QPushButton, QComboBox
from clients_subsystem.rii.database.CathedraModule import Cathedra
from clients_subsystem.rii.database.ClientModule import Client

class TeacherForm(QWidget):
    def __init__(self, id=0, parent = 0):
        super().__init__()
        self.initUI()
        self.ID=id
        self.Parent = parent
        if id:
            self.loadTeacherData()


    def initUI(self):
        self.vLay = QVBoxLayout()

        self.fioL = QLabel('ФИО')
        self.fioLE = QLineEdit()
        self.hl=QHBoxLayout()
        self.hl.addWidget(self.fioL)
        self.hl.addWidget(self.fioLE)
        self.vLay.addLayout(self.hl)

        self.h11 = QHBoxLayout()
        self.lShort = QLabel('Фамилия И.О.')
        self.leShort = QLineEdit()
        self.h11.addWidget(self.lShort)
        self.h11.addWidget(self.leShort)
        self.vLay.addLayout(self.h11)

        self.dolzhnostL = QLabel('Должность');
        self.dolzhnostLE = QLineEdit()
        self.h2 = QHBoxLayout()
        self.h2.addWidget(self.dolzhnostL)
        self.h2.addWidget(self.dolzhnostLE)
        self.vLay.addLayout(self.h2)

        self.obrazovanieL = QLabel('Образование')
        self.obrazovanieLE = QLineEdit()
        self.h3 = QHBoxLayout()
        self.h3.addWidget(self.obrazovanieL)
        self.h3.addWidget(self.obrazovanieLE)
        self.vLay.addLayout(self.h3)

        self.stepenL = QLabel("Степень")
        self.stepenLE = QLineEdit()
        self.h4 = QHBoxLayout()
        self.h4.addWidget(self.stepenL)
        self.h4.addWidget(self.stepenLE)
        self.vLay.addLayout(self.h4)

        self.zvanieL = QLabel('Звание')
        self.zvanieLE = QLineEdit()
        self.h5 = QHBoxLayout()
        self.h5.addWidget(self.zvanieL)
        self.h5.addWidget(self.zvanieLE)
        self.vLay.addLayout(self.h5)

        self.kvalifikaciaL = QLabel('Квалификация')
        self.kvalifikaciaLE = QLineEdit()
        self.h6 = QHBoxLayout()
        self.h6.addWidget(self.kvalifikaciaL)
        self.h6.addWidget(self.kvalifikaciaLE)
        self.vLay.addLayout(self.h6)

        self.kathL = QLabel('Кафедра')
        self.kathCB = QComboBox()
        self.cathData = Cathedra().getData()
        self.kathCB.addItems([rec['name'] for rec in self.cathData])
        self.h7 = QHBoxLayout()
        self.h7.addWidget(self.kathL)
        self.h7.addWidget(self.kathCB)
        self.vLay.addLayout(self.h7)

        self.savePB = QPushButton('Сохранить')
        self.vLay.addWidget(self.savePB)
        self.savePB.clicked.connect(self.save)

        self.setLayout(self.vLay)

        self.setWindowTitle('Добавление нового преподавателя')

    def loadTeacherData(self):
        data = Client().getFromID(self.ID)
        self.fioLE.setText(data['fio'])
        self.leShort.setText(data['shortfio'])
        self.dolzhnostLE.setText(data['dolzhnost'])
        self.obrazovanieLE.setText(data['obrazovanie'])
        self.stepenLE.setText(data['stepen'])
        self.zvanieLE.setText(data['zvanie'])
        self.kvalifikaciaLE.setText(data['kvalifikacia'])
        for i in range(len(self.cathData)):
            if data['idCath'] == self.cathData[i]['id']:
                self.kathCB.setCurrentIndex(i)
        self.setWindowTitle('Редактирование преподавателя')


    def save(self):
        ind  = self.kathCB.currentIndex()
        if ind==-1:
            ind=0
        idCath = self.cathData[ind]['id']

        if self.ID:
           Client().updateTeacher( idClient=self.ID,
                                 fio=self.fioLE.text(),
                                 shortfio=self.leShort.text(),
                                 obrazovanie=self.obrazovanieLE.text(),
                                 stepen=self.stepenLE.text(),
                                 zvanie=self.zvanieLE.text(),
                                 kvalifikacia=self.kvalifikaciaLE.text(),
                                 dolzhnost=self.dolzhnostLE.text(),
                                 idCath=idCath)
        else:
            Client().insertTeacher(fio=self.fioLE.text(),
                                 shortfio=self.leShort.text(),
                                 obrazovanie=self.obrazovanieLE.text(),
                                 stepen=self.stepenLE.text(),
                                 zvanie=self.zvanieLE.text(),
                                 kvalifikacia=self.kvalifikaciaLE.text(),
                                 dolzhnost=self.dolzhnostLE.text(),
                                 idCath=idCath)

        if self.Parent:
            self.Parent.RefreshTable()
        self.close()


