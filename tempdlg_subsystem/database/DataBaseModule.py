# -*- coding: utf-8 -*-
import mysql.connector

from PyQt5 import QtCore
from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser
from PyQt5.QtGui import QStandardItemModel, QStandardItem



def read_db_config(filename='tempdlg_subsystem//database//mysql.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db

def ConnectToDataBase(ex=0):
    # Данные по подключению к БД
    f=open('tempdlg_subsystem//database//mysql.txt','r')
    cs = f.read()
    f.close()
    cs =cs.split(';')
    #db= mysql.connector.connect(host='localhost',database='mysql',user='root',password='')

    try:
        db = mysql.connector.connect(host=cs[0], user=cs[1], passwd=cs[2], database=cs[3])
      #  db.set_character_set(cs[4])

    except mysql.connector.Error as err:
        print("Connection error: {}".format(err))
        try:
            db.close()
        except:
            db =0

    try:
        cur = db.cursor(dictionary=True)
        if ex:
            return [cur,db]
        return cur

    except mysql.connector.Error as err:
        return  -1
        print("Query error: {}".format(err))



def GetData(sql):
    '''Выполнить запрос и вернуть кортеж из словарей'''
    #cur = ConnectToDataBase()
    #cur.execute(sql)
    #data = cur.fetchall()
    data = [{" ": "Подключение не удалось"}]
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)

        row = cursor.fetchone()
        data = []
        while row is not None:
            data.append(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

    return data


def ExecuteSQL(sql):
    '''Выаолняет запрос.
        Возвращает индекс последней добавленной записи
        через INSERT
    db = ConnectToDataBase(1) #[cur, db]
    db[0].execute(sql)
    db[0].execute('SELECT LAST_INSERT_ID();')
    id = db[0].fetchall()
    db[1].commit()
    return id[0]['LAST_INSERT_ID()']
    '''
    lastID=0
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(sql)

        if cursor.lastrowid:
            lastID = cursor.lastrowid
            #print('last insert id', lastID)
        #else:
            #print('last insert id not found')


        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
    return lastID


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






