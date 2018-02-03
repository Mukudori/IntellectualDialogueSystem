from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

class SettingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.hblAdr = QHBoxLayout()
        self.labAdr = QLabel('Адрес')
        self.leAdr = QLineEdit()
        self.hblAdr.addWidget(self.labAdr)
        self.hblAdr.addWidget(self.leAdr)

        self.hblName = QHBoxLayout()
        self.labName = QLabel('Пользователь')
        self.leName = QLineEdit()
        self.hblName.addWidget(self.labName)
        self.hblName.addWidget(self.leName)

        self.hblPass = QHBoxLayout()
        self.labPass = QLabel('Пароль')
        self.lePass = QLineEdit()
        self.hblPass.addWidget(self.labPass)
        self.hblPass.addWidget(self.lePass)

        self.hblDB = QHBoxLayout()
        self.labDB = QLabel('База данных')
        self.leDB = QLineEdit()
        self.hblDB.addWidget(self.labDB)
        self.hblDB.addWidget(self.leDB)

        self.hblChar = QHBoxLayout()
        self.labChar = QLabel('Кодировка')
        self.leChar = QLineEdit()
        self.hblChar.addWidget(self.labChar)
        self.hblChar.addWidget(self.leChar)

        self.mainLay = QVBoxLayout()
        self.mainLay.addLayout(self.hblAdr)
        self.mainLay.addLayout(self.hblName)
        self.mainLay.addLayout(self.hblPass)
        self.mainLay.addLayout(self.hblDB)
        self.mainLay.addLayout(self.hblChar)

        self.pb = QPushButton('Сохранить')
        self.pb.clicked.connect(self.WriteData)
        self.mainLay.addWidget(self.pb)

        self.setLayout(self.mainLay)
        self.setWindowTitle('Настройка подключения к базе данных')


        self.ReadData()

    def ReadData(self):
        f = open('database//mysql.txt', 'r')
        text = f.read()
        f.close()
        text = text.split(';')
        self.leAdr.setText(text[0])
        self.leName.setText(text[1])
        self.lePass.setText(text[2])
        self.leDB.setText(text[3])
        self.leChar.setText(text[4])

    def WriteData(self):
        f = open('database//mysql.txt', 'w')
        f.write(self.leAdr.text()+';'+
                self.leName.text()+';'+
                self.lePass.text()+';'+
                self.leDB.text()+';'+
                self.leChar.text()+';')
        f.close()
        self.close()

