from PyQt5.QtWidgets import QApplication
from clients_subsystem.rii.RIIDBMainFormModule import RIIDataBaseForm
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RIIDataBaseForm()
    ex.show()
    sys.exit(app.exec_())