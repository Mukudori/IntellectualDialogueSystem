import importlib
#from tempdlg_subsystem.temp_logic import scrypts

def dynamic_import(module):
    return importlib.import_module(module)

def GetAnswer(name_module, mainLogic=0):
    module = dynamic_import('tempdlg_subsystem.temp_logic.scrypts.'+name_module)
    return module.GetAnswer(mainLogic)

if __name__ == '__main__':
    print (GetAnswer('id_4.py'))