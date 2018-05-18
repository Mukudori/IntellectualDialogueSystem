from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout,\
    QLineEdit, QPushButton
from clients_subsystem.rii.database.AuditoryModule import Auditory

class AddAuditoryDialog(QWidget):
    def __init__(self, parent=0):
        super().__init__()
        self.initUI()
        self.Parent=parent

    def initUI(self):
        vLay = QVBoxLayout()
        hl = QHBoxLayout()
        self.lab = QLabel('Номер аудитории : ')
        self.le = QLineEdit()
        hl.addWidget(self.lab)
        hl.addWidget(self.le)
        self.pb = QPushButton('Добавить')
        vLay.addLayout(hl)
        vLay.addWidget(self.pb)

        self.setLayout(vLay)
        self.setWindowTitle('Добавление аудитории')

        self.pb.clicked.connect(self.insertAuditory)

    def insertAuditory(self):
        Auditory().insertRecord(numAuditory=self.le.text())
        if self.Parent:
            self.Parent.RefreshTable()
        self.close()
