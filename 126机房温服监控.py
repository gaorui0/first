import requests
import json
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from suds.client import Client  

def Request_information():
    url = 'http://202.206.32.100/getdata'
    headers = {
        'Cookie': 'user=admin',
        'Host': '202.206.32.100',
        'Origin': 'http://202.206.32.100',
        'Referer': 'http://202.206.32.100/Main.html',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Mobile Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }


    data = {
        'titleName': 'Main'
    }
    response = requests.post(url=url,headers=headers,data=data)
    print(response.json()[0][20])
    JsonStr = json.dumps( response.json(), ensure_ascii=False) 

    Arr = json.loads(JsonStr)

    
    subject1 = Arr[26]['value']
    subject1 = float(subject1)
    subject2 = Arr[43]['value']
    subject2 = float(subject2)
    subject3 = Arr[47]['value']
    subject3 = float(subject3)
    subject4 = Arr[51]['value']
    subject4 = float(subject4)
    subject5 = Arr[22]['data'][0][1]
    subject6 = Arr[22]['data'][0][4]


        # os.system('zabbix_sender -z 192.168.255.211 -s "stuNO1_1F_1" -k trapper_temperature1 -o %s'%subject1)
        # os.system('zabbix_sender -z 192.168.255.211 -s "stuNO1_1F_1" -k trapper_temperature2 -o %s'%subject2)
        # os.system('zabbix_sender -z 192.168.255.211 -s "stuNO1_1F_1" -k trapper_temperature3 -o %s'%subject3)
        # os.system('zabbix_sender -z 192.168.255.211 -s "stuNO1_1F_1" -k trapper_temperature4 -o %s'%subject4)
        # os.system('zabbix_sender -z 192.168.255.211 -s "stuNO1_1F_1" -k trapper_gaojing -o %s'%subject5)
        # os.system('zabbix_sender -z 192.168.255.211 -s "stuNO1_1F_1" -k trapper_gaojing -o %s'%subject6)
    if subject1 > 30 or subject2 > 30 or subject3 > 31 or subject4 > 30:
        sendmessage(subject1,subject2,subject3,subject4)

       

    # else:
    #     subject7 = (Arr[39]['value'])
    #     os.system('zabbix_sender -z 192.168.255.211 -s "stuNO1_1F_1" -k trapper_dianya -o %s'%subject7)


def sendmessage(subject1,subject2,subject3,subject4):
    
    url = 'http://www.hebxxt.com/hdxxt/ADCService/XxtService?wsdl'
    client = Client(url)
    data = '当前机房南1温度为:%0.2f\n,当前机房南2温度为%0.2f\n,当前机房南3温度为%0.2f\n,当前机房南4温度为%0.2f' %(subject1,subject2,subject3,subject4)
    mobile = ['15130085363','18034534001'] 
    
    for ipone in mobile:

        person_added = client.service.SendSms('XXT915074','15511336200','15511336200',ipone,data,0)

if __name__ == '__main__':
    

    scheduler = BackgroundScheduler()

## '0:00-2:00，6:00-8:00，12:00-14:00和18:00-20:00'

    scheduler.add_job(Request_information,'cron',  hour='0-23',minute='*/30') 



    scheduler.start()


    try:

        # This is here to simulate application activity (which keeps the main thread alive).

        while True:

            time.sleep(10)  #其他任务是独立的线程执行
        

    except (KeyboardInterrupt, SystemExit):

        # Not strictly necessary if daemonic mode is enabled but should be done if possible

        scheduler.shutdown()

        print('Exit The Job!')

        
    







# s = json.dumps(response.text)
# print(type(s))

# m = json.loads(s)

# print(type(m))

# print(Arr[39]['value'])

# print(Arr[78]['value']) #   B输入电压