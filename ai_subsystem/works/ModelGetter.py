from configparser import ConfigParser
import os

def getActiveModelName():
    workPath = os.path.abspath(os.curdir) + '/ai_subsystem/works/'
    parserActivated = ConfigParser()
    path_model =workPath+'activated.ini'
    parserActivated.read(path_model)
    if parserActivated.has_section('activated-model'):
      return parserActivated.items('activated-model')[0][1]
