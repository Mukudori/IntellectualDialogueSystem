import importlib

def dynamic_import(module):
    return importlib.import_module(module)

def GetAnswer(name_module, *args):
    module = dynamic_import('tempdlg_subsystem.temp_logic.scrypts.'+name_module)
    return module.execute(args)

#if __name__ == '__main__':
#    print (GetAnswer('id_4.py'))