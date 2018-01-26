from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5 import QtGui


class MessageWidget (QWidget):
    def __init__ (self, parent = None):
        super(MessageWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel    = QLabel()
        self.textDownQLabel  = QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QHBoxLayout()
        self.iconQLabel      = QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)


    def setTextUp (self, text, color = 'color: rgb(0, 0, 255);'):
        self.textUpQLabel.setText(text)
        self.textUpQLabel.setStyleSheet(color)

    def setTextDown (self, text, color = 'color: rgb(0, 0, 0)'):
        self.textDownQLabel.setText(text)
        self.textDownQLabel.setStyleSheet(color)

    def setIcon (self, imagePath):
        self.iconQLabel.setPixmap(QtGui.QPixmap(imagePath))
