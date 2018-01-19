import MySQLdb
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore
import WordTableModule

#Данные по подключению к БД
connStr = '127.0.0.1;root;4862159357;botdb;utf8'

'''
    В Qt ксть встроенные медоды для работы с MySQL и построения моделей таблиц, 
    но, так как драйвер БД требует плясок с бубном и не с разными версиями Python могут возникнуть сложности,
    я решил не запариваться по этому поводу и строить модели вручную.
'''

def ConnectToDataBase():
    cs = connStr.split(';')
    try:
        conn = MySQLdb.connect(host=cs[0], user=cs[1], passwd=cs[2], db=cs[3])
        conn.set_character_set(cs[4])

    except MySQLdb.Error as err:
        print("Connection error: {}".format(err))
        conn.close()

    try:
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        return cur

    except MySQLdb.Error as err:
        return  -1
        print("Query error: {}".format(err))



def GetData(sql):
    '''Выполнить запрос и вернуть кортеж из словарей'''
    cur = ConnectToDataBase()
    cur.execute(sql)
    data = cur.fetchall()
    return data

def ExecuteSQL(sql):
    '''Выполнить запрос'''
    cur = ConnectToDataBase()
    cur.execute(sql)


def GetTableViewModel(sql, table='tab'):
    '''
    Функция подключается к БД, строит Модель по всем полям
    Так как MySQL любит перепутывать поля мне пришлось учитывать позицию id записи.
    :param sql: Запрос
    :param table: Не обязательный параметр для перевода закодированных строк ы dialogtab
    :return: возвращает массив из Модели и позиции id
    '''
    data  = GetData(sql)
    model = QStandardItemModel()
    horhead = list(data[0].keys())
    model.setHorizontalHeaderLabels(horhead)
    model.setVerticalHeaderLabels([' ']*len(data))

    for i in range(len(data)):
        for j in range(len(horhead)):
            item = QStandardItemModel()

            if table == 'dialogtab' and (horhead[j] == 'question' or horhead[j] == 'answer'):
                wt = WordTableModule.WordTable()
                item = QStandardItem(wt.GetDecodeText(data[i][horhead[j]]))
            else:
                item = QStandardItem(str(data[i][str(horhead[j])]))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, j, item)
    for idPose in range(len(horhead)):
        if horhead[idPose] == 'id': break
    return [model,idPose]







