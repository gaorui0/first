import serial
import minimalmodbus
import struct
import time
import pymysql
import threading
from datetime import datetime
import binascii
import socket


def  val():
    global wd
    global sd
    global bs
    #sj = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  
    collect_command=[0x01,0x03,0x00,0x04,0x00,0x02,0x85,0xCA]
    send_command=struct.pack("%dB" % (len(collect_command)),*collect_command)
    ser=serial.Serial("com1",9600,timeout=0.5)  
    ser.bytesize = 8
    ser.stopbits =1
    ser.write(send_command)
    bs = ser.readline()
    ser.close()
    #bs = str(bs.decode('utf8'))
    print(type(bs))
    wd = int.from_bytes(bs[3:5],'big')
    sd = int.from_bytes(bs[5:7],'big')
    wd = ((wd/1000-4)/(20-4))*100-20
    wd = '%0.2f'%wd
    sd = ((sd/1000-4)/(20-4))*100
    sd = '%0.2f'%sd
    print(wd)
    print(sd)
    
    #fx = bs[3:6]
    #fs = bs[7:13]


def power_off():

    print('Trun Off Power')
    time.sleep(10)
    power_controller_address = ('192.168.0.199', 12345)
    power_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    power_s.connect(power_controller_address)

    #close temperaure  power
    data='AT+STACH2=0\r\n'
    power_s.send(data.encode())
    msg = power_s.recv(20)
    print (msg.decode('utf-8'))

    power_s.close()


def power_on():
    print('Trun On Power')

    power_controller_address = ('192.168.0.199', 12345)
    power_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    power_s.connect(power_controller_address)

    #open temperauter  power

    data='AT+STACH2=1\r\n'
    power_s.send(data.encode())
    msg = power_s.recv(20)
    print (msg.decode('utf-8'))

        
    power_s.close()


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
            if len(bs) == 0:
                power_off()
                time.sleep(60)
                power_on()
                time.sleep(60)
                val()
                i = i + 1
            else:
                break


        
        
        conn,cursor = get_conn()
        #time=str(datetime.now())
        collect_time = datetime.now()
        # sql = 'insert into w(time,fu,fx) \ values(%s,%s%s)'%(time,fu,fx)
        sql = "insert into tempurature(collect_time,wd,sd) \
                values('%s','%s','%s')" % (collect_time,wd,sd)
        cursor.execute(sql)

        conn.commit()
        close(conn,cursor)
            
        timeArray = time.strftime("%Y-%m-%d %H:%M:%S")
        data = timeArray + ',' + wd + ',' + sd
        file = r'D:\temperature1.txt'
        with open(file,'a+') as f:
            f.writelines(data + '\n')
        
        time.sleep(1800)
    except IOError:
        print('not value')
        continue
    



        



    
   