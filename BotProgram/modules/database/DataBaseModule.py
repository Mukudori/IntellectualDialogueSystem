import MySQLdb
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore
from database import DlgTableModule

#Данные по подключению к БД
connStr = '127.0.0.1;root;4862159357;botdb;utf8'

'''
    В Qt есть встроенные медоды для работы с MySQL и построения моделей таблиц, 
    но, так как драйвер БД требует плясок с бубном и с разными версиями Python могут возникнуть сложности,
    я решил не запариваться по этому поводу и строить модели вручную.
'''

def ConnectToDataBase(ex=0):
    cs = connStr.split(';')
    try:
        db = MySQLdb.connect(host=cs[0], user=cs[1], passwd=cs[2], db=cs[3])
        db.set_character_set(cs[4])

    except MySQLdb.Error as err:
        print("Connection error: {}".format(err))
        db.close()

    try:
        cur = db.cursor(MySQLdb.cursors.DictCursor)
        if ex:
            return [cur,db]
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
    '''Выаолняет запрос.
        Возвращает индекс последней добавленной записи
        через INSERT'''
    db = ConnectToDataBase(1) #[cur, db]
    db[0].execute(sql)
    db[0].execute('SELECT LAST_INSERT_ID();')
    id = db[0].fetchall()
    db[1].commit()
    return id[0]['LAST_INSERT_ID()']






