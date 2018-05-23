from tempdlg_subsystem.database.UserGroupModule import UserGroupTable
from tempdlg_subsystem.database.AccessTableModule import AccessTable
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QWidget,QPushButton, \
    QVBoxLayout,QComboBox, QMessageBox

class AddGroupDlg(QWidget):
    def __init__(self, tableView, model, idContext):
        super().__init__()
        self.lay = QVBoxLayout()
        self.cb = QComboBox()
        self.but = QPushButton("Добавить")
        self.lay.addWidget(self.cb)
        self.lay.addWidget(self.but)
        self.setLayout(self.lay)
        self.setWindowTitle("Добавление группы в контекст")

        self.but.clicked.connect(self.click)

        self.tv = tableView
        self.Model = model
        self.idCon = idContext
        self.Groups = UserGroupTable().GetStringAndIDList()
        self.cb.addItems([row[1] for row in self.Groups])
        self.GroupIDList = AccessTable().GetIDGroupListFromIDContext(idContext)

    def click(self):
        idGroup = 0
        for row in self.Groups:
            if row[1] == self.cb.currentText():
                idGroup = row[0]
                break
        if idGroup not in self.GroupIDList:
            AccessTable().AddRecord(idGroup=idGroup, idContext=self.idCon)
            i = self.Model.rowCount()
            self.Model.setItem(i, 1, QStandardItem(self.cb.currentText()))
            self.Model.setItem(i, 0, QStandardItem(str(idGroup)))
            self.Model.setVerticalHeaderLabels([' '] * (i+1))
            self.close()
        else:
            self.qmb = QMessageBox()
            self.qmb.about(self, 'Ошибка', 'Группа пользователей уже имеет доступ к этому контексту.')
