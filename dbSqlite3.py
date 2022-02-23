# -*- coding: utf-8 -*-
import sqlite3

def OpenDb():
    database = "./db/student_083_2.db"
    # database = "./db/student_083.db"
    conn = sqlite3.connect(database)
    # conn.row_factory = sqlite3.Row
    return conn



def GetSql(conn, sql):

    cur = conn.cursor()
    cur.execute(sql)
    fields=[]
    for field in cur.description:
        fields.append(field[0])

    result = cur.fetchall()
    # for item in result:
    #     print(item)
    cur.close()
    return result,fields


def CloseDb(conn):
    conn.close()


def GetSql2(sql):
    conn = OpenDb()
    result,fields = GetSql(conn, sql)
    CloseDb(conn)
    return result,fields


def UpdateData(data, tablename):
    conn = OpenDb()
    values = []
    cusor = conn.cursor()
    idName = list(data)[0]
    for v in list(data)[1:]:
        values.append("%s='%s'" % (v, data[v]))
    sql = "update %s set %s where %s='%s'" % (tablename, ",".join(values), idName, data[idName])
    # print (sql)
    cusor.execute(sql)
    conn.commit()
    CloseDb(conn)


def InsertData(data, tablename):
    conn = OpenDb()
    values = []
    cusor = conn.cursor()
    fieldNames = list(data)
    for v in fieldNames:
        values.append(data[v])
    sql = "insert into  %s (%s) values( %s) " % (tablename, ",".join(fieldNames), ",".join(["?"] * len(fieldNames)))
    # print(sql)
    cusor.execute(sql, values)
    conn.commit()
    CloseDb(conn)


def DelDataById(id, value, tablename):
    conn = OpenDb()
    values = []
    cusor = conn.cursor()

    sql = "delete from %s  where %s=?" % (tablename, id)
    # print (sql)

    cusor.execute(sql,(value,))
    conn.commit()
    CloseDb(conn)
