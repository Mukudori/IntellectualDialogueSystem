from sys import argv, exit
from ai_subsystem.aiMainFormModule import AiMainForm
from PyQt5.QtWidgets import QApplication
from ai_subsystem import ai
if __name__ == '__main__':
    if len(argv) == 1:
        app = QApplication(argv)
        ex = AiMainForm()
        ai.parent_form = ex
        ex.show()
        exit(app.exec_())
    elif len(argv)<5:
        pass
    else:
        ai.main()

