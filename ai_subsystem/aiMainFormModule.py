import os
import sys
import subprocess
from ai_subsystem import  ai
import os
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel,\
  QHBoxLayout, QVBoxLayout, QListWidgetItem, QLineEdit,\
  QPushButton, QMessageBox, QDialog
from PyQt5 import uic
from configparser import ConfigParser
from ai_subsystem.editModelFormModule import EditModelForm
import shutil
import gzip




class ModelWidget(QWidget):
  def __init__(self, name,parserItems = 0, activate = False):
    super().__init__()

    self.labNam =QLabel(name)
    self.labIco = QLabel("<img src=pics/model.png width = 64>")
    if activate:
      actText = "<font color = 'blue'> Активная модель</font>"
    else:
      actText = str()
    self.labActivate = QLabel(actText)
    self.vLay = QVBoxLayout()
    self.hLay = QHBoxLayout()
    self.hLay.addWidget(self.labIco)
    self.hLay.addWidget(self.labNam)
    self.vLay.addLayout(self.hLay)
    self.vLay.addWidget(self.labActivate)
    self._initParser(parserItems)
    self.setLayout(self.vLay)


  def _initParser(self, items):
    if items:
      self.labData = QLabel('Дата последнего обучения : '+items[1][1])
      self.Size = QLabel('Размерность модели : %sx%s' % (items[2][1], items[3][1]))
      self.vLay.addWidget(self.labData)
      self.vLay.addWidget(self.Size)
    else:
      self.labInfoNotFound  = QLabel('Файл modelinfo.ini поврежден или не найден')
      self.labInfoNotFound.setWordWrap(True)
      self.vLay.addWidget(self.labInfoNotFound)


class CreateModelForm(QWidget):
  def __init__(self, parent =0):
    super().__init__()
    self.lineEdit = QLineEdit()
    self.label = QLabel('Введите название модели')
    self.button = QPushButton('Создать')
    self.lay = QVBoxLayout()
    self.lay.addWidget(self.label)
    self.lay.addWidget(self.lineEdit)
    self.lay.addWidget(self.button)
    self.setLayout(self.lay)
    self.button.clicked.connect(self.CreateWorkspace)
    self.Parent = parent

  def keyPressEvent(self, event):
    key = event.key()
    if key == 16777220:  # код клавиши Enter
      self.CreateWorkspace()


  def CreateWorkspace(self):
    worksdir = os.path.abspath(os.curdir) + '/ai_subsystem/works/'+self.lineEdit.text()+'/'
    directory = os.path.dirname(worksdir)
    if os.path.exists(directory):
      self.msg = QMessageBox()
      self.msg.setIcon(QMessageBox.Information)
      self.msg.setText("Ошибка")
      self.msg.setInformativeText("Модель уже существует")
      self.msg.setWindowTitle("Ошибка")
      self.msg.show()
    else:
      os.makedirs(directory)
      directory = os.path.dirname(worksdir+'/data/')
      os.makedirs(directory)
      directory = os.path.dirname(worksdir+'/data/train/')
      os.makedirs(directory)
      directory = os.path.dirname(worksdir + '/data/test/')
      os.makedirs(directory)
      if self.Parent:
        self.Parent.refreshListWidget()
      f_zip = gzip.open("%s/data/train/chat.txt.gz" % worksdir, 'w')
      f_zip.close()

    self.close()

class Y_N_Dialog(QDialog):
  def __init__(self, parent):
    super().__init__()
    self.Parent = parent
    self.label = QLabel("Вы действительно хотите удалить модель?\n ВСЯ информация о модели будет удалена без возможности востановления.")
    self.bY = QPushButton('Да')
    self.bN = QPushButton('Нет')
    self.layH = QHBoxLayout()
    self.layV = QVBoxLayout()
    self.layH.addWidget(self.bN)
    self.layH.addWidget(self.bY)
    self.layV.addWidget(self.label)
    self.layV.addLayout(self.layH)
    self.setLayout(self.layV)
    self.bY.clicked.connect(self.Yes)
    self.bN.clicked.connect(self.No)
    self.setWindowTitle('Предупреждение')

  def Yes(self):
    self.Parent.deleteModel()
    self.close()
  def No(self):
    self.close()

class AiMainForm(QMainWindow):
  def __init__(self):
    super(AiMainForm, self).__init__()
    uic.loadUi("ai_subsystem/ui/aiForm.ui", self)
    self.worksdir = os.path.abspath(os.curdir)+'/ai_subsystem/works/'


    self.refreshListWidget()

    self.getDeviseInfo()

    self.act_Add.triggered.connect(self.showCreateModelForm)
    self.act_Refresh.triggered.connect(self.showEditModelForm)
    self.act_Del.triggered.connect(self.runDeleteDialog)

  def refreshListWidget(self):
    parserActivated = ConfigParser()
    path_model = self.worksdir + 'activated.ini'
    parserActivated.read(path_model)
    if parserActivated.has_section('activated-model'):
      name_activated_model = parserActivated.items('activated-model')[0][1]
    self.namelist = []
    self.listWidget.clear()
    for model in os.listdir(self.worksdir):
      if os.path.isdir(self.worksdir + model):
        itemsInfo=0
        try:
          parserModel = ConfigParser()
          parserModel.read(self.worksdir + model+'/modelinfo.ini')
          itemsInfo = parserModel.items('modelinfo')
        except:
          print('файл %s/modelinfo.ini поврежден или не найден' % self.worksdir )


        self.namelist.append(model)
        mwid = ModelWidget(model, parserItems=itemsInfo, activate=name_activated_model == model)
        myQListWidgetItem = QListWidgetItem(self.listWidget)

        myQListWidgetItem.setSizeHint(mwid.sizeHint())

        self.listWidget.addItem(myQListWidgetItem)
        self.listWidget.setItemWidget(myQListWidgetItem, mwid)


  def showEditModelForm(self):
    self.childF = EditModelForm(modelName=self.namelist[self.listWidget.currentRow()], parent=self)
    self.childF.show()

  def showCreateModelForm(self):
    self.childF = CreateModelForm(parent=self)
    self.childF.show()

  def runDeleteDialog(self):
    self.delDialog = Y_N_Dialog(self)
    self.delDialog.show()

  def deleteModel(self):
    path = self.worksdir + self.namelist[self.listWidget.currentRow()]
    try:
      shutil.rmtree(path)
      self.refreshListWidget()
    except:
      self.msg = QMessageBox()
      self.msg.setIcon(QMessageBox.Information)
      self.msg.setText("Ошибка")
      self.msg.setInformativeText("не удалось удалить модель")
      self.msg.show()

  def showDialog(self):
    pass

  def getDeviseInfo(self):
    pass


