import importlib

def dynamic_import(module):
    return importlib.import_module(module)

def GetAnswer(name_module, *args):
    # Динамическое подключение скрипта
   # try:
    module = dynamic_import('tempdlg_subsystem.temp_logic.scrypts.'
                                + name_module)
    #except:
   #     return 'Ошибка! Файл сценария поврежден или удален.'
    # Исполнение скрипта
    #try:
    return module.execute(args)
    #except:
    #    return "Произошла ошибка во время выполнения сценария."
