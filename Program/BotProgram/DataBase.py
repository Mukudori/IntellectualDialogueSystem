import MySQLdb
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore

#Данные по подключению к БД
connStr = '127.0.0.1;root;4862159357;botdb;utf8'

#Выполнить запрос и вернуть кортеж из словарей
def GetData(sql):
    cs = connStr.split(';')
    try:
        conn = MySQLdb.connect(host=cs[0], user=cs[1], passwd=cs[2], db=cs[3])
        conn.set_character_set(cs[4])

    except MySQLdb.Error as err:
        print("Connection error: {}".format(err))
        conn.close()

    try:
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(sql)
        data = cur.fetchall()

    except MySQLdb.Error as err:
        print("Query error: {}".format(err))
    return data

def GetTableViewModel(sql, table='tab'):
    data  = GetData(sql)
    model = QStandardItemModel()
    horhead = list(data[0].keys())
    model.setHorizontalHeaderLabels(horhead)

    for i in range(len(data)):
        for j in range(len(horhead)):
            item = QStandardItemModel()
            if table == 'dialogtab' and (horhead[j] == 'question' or horhead[j] == 'answer'):
                item = QStandardItem(GetTextFromCodes(data[i][horhead[j]]))
            else:
                item = QStandardItem(str(data[i][str(horhead[j])]))
            model.setItem(i, j, item)
    return model

    #Преобразовать закодированную строку в текст
def GetTextFromCodes(codeText):
    codeStr = codeText.split(';')
    outS = str()
    for s in codeStr:
        wordid = s.split(' ')
        if wordid != ['']:
            for word in wordid:
                data = GetData("select word from wordtab"+
                    " where idGroup='"+word.split('-')[0]+
                    "' and id='"+word.split('-')[1]+"'")
                outS=outS+data[0]['word']+' '
                outS = outS + ';'
    return outS