import os
import sys
import subprocess
from ai_subsystem import  ai
import os
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QListWidgetItem
from PyQt5 import uic
from configparser import ConfigParser
from ai_subsystem.editModelFormModule import EditModelForm

from tensorflow.python.client import device_lib

import tempfile


class ModelWidget(QWidget):
  def __init__(self, name, activate = False):
    super().__init__()

    self.labNam =QLabel(name)
    self.labIco = QLabel("<img src=pics/model.png width = 64>")
    if activate:
      actText = "<font color = 'green'> Активная модель</font>"
    else:
      actText = str()
    self.labActivate = QLabel(actText)
    self.vLay = QVBoxLayout()
    self.hLay = QHBoxLayout()
    self.hLay.addWidget(self.labIco)
    self.hLay.addWidget(self.labNam)
    self.vLay.addLayout(self.hLay)
    self.vLay.addWidget(self.labActivate)
    self.setLayout(self.vLay)



class AiMainForm(QMainWindow):
  def __init__(self):
    super(AiMainForm, self).__init__()
    uic.loadUi("ai_subsystem/ui/aiForm.ui", self)
    worksdir = os.path.abspath(os.curdir)+'/ai_subsystem/works/'
    parser = ConfigParser()
    path_model =worksdir+'activated.ini'
    parser.read(path_model)
    if parser.has_section('activated-model'):
      name_activated_model = parser.items('activated-model')[0][1]

    self.namelist = []
    for model in os.listdir(worksdir):
      if os.path.isdir(worksdir+model):
        self.namelist.append(model)
        mwid = ModelWidget(model, activate=name_activated_model==model)
        myQListWidgetItem = QListWidgetItem(self.listWidget)

        myQListWidgetItem.setSizeHint(mwid.sizeHint())

        self.listWidget.addItem(myQListWidgetItem)
        self.listWidget.setItemWidget(myQListWidgetItem, mwid)

    self.getDeviseInfo()

    self.act_Add.triggered.connect(self.showCreateModelForm)
    self.act_Refresh.triggered.connect(self.showEditModelForm)


  def showEditModelForm(self):

    self.childF = EditModelForm(modelName=self.namelist[self.listWidget.currentRow()])
    self.childF.show()
  def showCreateModelForm(self):
    self.childF = EditModelForm()
    self.childF.show()

  def showDialog(self):
    pass

  def getDeviseInfo(self):
    pass


