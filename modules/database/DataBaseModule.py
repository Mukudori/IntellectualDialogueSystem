# -*- coding: utf-8 -*-
import MySQLdb
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore

'''
    В Qt есть встроенные медоды для работы с MySQL и построения моделей таблиц, 
    но, так как драйвер БД требует плясок с бубном и с разными версиями Python могут возникнуть сложности,
    я решил не запариваться по этому поводу и строить модели вручную.
'''

def ConnectToDataBase(ex=0):
    # Данные по подключению к БД
    f=open('modules//database//mysql.txt','r')
    cs = f.read()
    f.close()
    cs =cs.split(';')
    db=MySQLdb.connect

    try:
        db = MySQLdb.connect(host=cs[0], user=cs[1], passwd=cs[2], db=cs[3])
        db.set_character_set(cs[4])

    except MySQLdb.Error as err:
        print("Connection error: {}".format(err))
        try:
            db.close()
        except:
            db =0

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

def CreateTableViewModel(sql, fieldTab, fieldsView):
    data = GetData(sql)
    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(fieldsView)
    model.setVerticalHeaderLabels([' '] * len(data))

    for i in range(len(data)):
        for j in range(len(fieldTab)):
            item = QStandardItem(str(data[i][fieldTab[j]]))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            model.setItem(i, j, item)

    return model






