import importlib
#from modules.bot import scrypts

def dynamic_import(module):
    return importlib.import_module(module)

def GetAnswer(name_module):
    module = dynamic_import(name_module)
    return module.GetAnswer()

if __name__ == '__main__':
    print (GetAnswer('id_4'))