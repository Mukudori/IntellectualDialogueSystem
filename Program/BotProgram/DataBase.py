import MySQLdb

#Данные по подключению к БД
connStr = '127.0.0.1;root;4862159357;botdb;utf8'

#Выполнить запрос и вернуть кортеж из словарей
def GetTable(sql):
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