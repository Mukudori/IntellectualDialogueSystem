from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,QCheckBox
from modules.database.UserGroupModule import UserGroupTable
class EditUserGroup(QWidget):
    def __init__(self, id=0):
        super().__init__()
        self.MainLayout = QVBoxLayout()

        self.grouplay = QHBoxLayout()
        self.labGroup = QLabel('Группа')
        self.leGroup = QLineEdit()
        self.grouplay.addWidget(self.labGroup)
        self.grouplay.addWidget(self.leGroup)

        self.MainLayout.addLayout(self.grouplay)
        self.editDB = QCheckBox('Редактировать БД')
        self.MainLayout.addWidget(self.editDB)
        self.butUpdate = QPushButton('Сохранить')
        self.butInsert = QPushButton('Добавить')


        self.butLay = QHBoxLayout()
        self.butLay.addWidget(self.butUpdate)
        self.butLay.addWidget(self.butInsert)
        self.table = UserGroupTable()
        if id:
            rec = self.table.GetDataFromID(id)
            self.editDB.setChecked(rec['editDB'])
            self.leGroup.setText(rec['nameGroup'])
            self.ID = id
            self.MainLayout.addWidget(self.butUpdate)

            self.butUpdate.clicked.connect(self.__Update)
            self.butInsert.setMaximumWidth(0)
        else:
            self.butInsert.clicked.connect(self.__Insert)
            self.butUpdate.setMaximumWidth(0)

        self.MainLayout.addLayout(self.butLay)

        self.setLayout(self.MainLayout)
        self.setWindowTitle('Редактирование группы пользователей')

    def __Update(self):
        self.table.UpdateRecord(id = self.ID, nameGroup = self.leGroup.text(),
                                editDB = 1 if self.editDB.isChecked() else 0)
        self.close()

    def __Insert(self):
        self.table.InsertRecord(nameGroup=self.leGroup.text(),
                                editDB=1 if self.editDB.isChecked() else 0)
        self.close()




