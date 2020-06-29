import pymysql
import threading
from datetime import datetime

def get_conn():
    conn = pymysql.connect(database="cov", user="root", password="123456", host='localhost', port=3306)
    cursor = conn.cursor()
    return conn,cursor


def close(conn,cursor):
    cursor.close()
    conn.close()

def tem():
    conn,cursor = get_conn()
    time = datetime.now()
    print(time)
    wd = '25.23'
    sd = '32.36%'
    # sql = 'insert into temperature(time,wd,sd) \ values(%s,%s%s)'%(time,wd,sd)
    sql = "insert into temperature(time,wd,sd) \
            values('%s','%s','%s')" % (time,wd,sd)
    cursor.execute(sql)

    conn.commit()
    close(conn,cursor)
