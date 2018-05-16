
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu
from PyQt5 import uic, QtCore

from clients_subsystem.rii.database.ClientModule import Client
from clients_subsystem.rii.database.CathedraModule import Cathedra
from clients_subsystem.rii.TeacherFormModule import TeacherForm
from clients_subsystem.rii.StudentFormModule import StudentForm
from clients_subsystem.rii.database.CathGroupModule import CathGroup
from clients_subsystem.rii.CathGroupFormModule import CathGroupForm
from clients_subsystem.rii.CathedraFormModule import CathedraForm
from clients_subsystem.rii.OpenTimeTableModule import OpenTimeTableForm

class TimeTableForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('clients_subsystem/rii/ui/TimeTableForm.ui', self)

    def initClient(self):
        pass