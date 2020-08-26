import serial
import minimalmodbus
import struct
import time
import pymysql
import threading
from datetime import datetime
import socket
import binascii


def  val():
    global fx
    global fs
    
    #sj = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  
    #collect_command=[0x01,0x03,0x00,0x04,0x00,0x02,0x85,0xCA]
    #send_command=struct.pack("%dB" % (len(collect_command)),*collect_command)
    ser=serial.Serial("com2",9600,timeout=0.5)  
    ser.bytesize = 8
    ser.stopbits =1
    #ser.write(send_command)
    #ser.open()
    bs = ser.readline()
    #time.sleep()
    ser.close()            #关闭com2
    #print(bs)
    bs = str(bs.decode('utf8'))
    print(type(bs))
    print(bs)
    fs = bs[3:8]           #取风速的值
    fx = bs[10:16]         #取风向的值
    #print(fs)
    #print(fx)


def get_conn():
    conn = pymysql.connect(database="cov", user="root", password="123456", host='localhost', port=3306)
    cursor = conn.cursor()
    return conn,cursor


def close(conn,cursor):
    cursor.close()
    conn.close()


while True:


    try:
        val()
        i = 1
        while (i < 10): 
            if len(fx) == 0:
                val()
                i = i + 1
            else:
                break

        print(fx)
        print(fs)
        
        
        conn,cursor = get_conn()
        #time=str(datetime.now())
        collect_time = datetime.now()
        
        # sql = 'insert into w(time,fu,fx) \ values(%s,%s%s)'%(time,fu,fx)
        sql = "insert into wind_speed(collect_time,fs,fx) \
                values('%s','%s','%s')" % (collect_time,fs,fx)
        cursor.execute(sql)

        conn.commit()
        close(conn,cursor)
            
        fx = fx + '°'
        fs = fs + 'm/s'
        timeArray = time.strftime("%Y-%m-%d %H:%M:%S")
        data = timeArray + ',' + fx + ',' + fs
        file = r'D:\wind_speed.txt'
        with open(file,'a+') as f:
            f.writelines(data + '\n')
        
        time.sleep(900)
    except IOError:
        print('not value')
        time.sleep(5)
        continue