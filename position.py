import smtplib
from  email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time
import ipinfo
import requests
import cv2


def network_requests():
    try:
        url = 'http://www.baidu.com'
        res = requests.get(url)
        if res.status_code == 200:
            return 1
    except:
        return 0


def getPics():
    cap = cv2.VideoCapture(0)
    ret,frame = cap.read()
    cv2.imwrite(r'D:\ima.jpg',frame)
    cap.release()


def sendMail():

    retVal = test(AK)
    con = smtplib.SMTP_SSL('smtp.qq.com',465)

    con.login('964717304@qq.com','wfkjbahuzdzhbdce')
    
    msg = MIMEMultipart()

    msg['Subject'] = Header('笔记本位置%s'%retVal,'utf-8').encode()
    msg['From'] = '964717304@qq.com'#这个随便写，主要是让对方知道你是谁
    msg['To'] = '964717304@qq.com'#收件信息


    image_date1 = open(r'D:\ima.jpg', "rb").read()
    image1 = MIMEImage(image_date1)

    image1["Content-Disposition"] = 'attachment;filename="123.jpg"'

    msg.attach(image1)
    con.sendmail('964717304@qq.com','964717304@qq.com',msg.as_string())
    con.quit()


def requests_ip():
    access_token = 'bb0246ed41fcb6'

    handler=ipinfo.getHandler(access_token)
    details=handler.getDetails()
    ip=details.ip

    return ip



def test(AK):
    ip = requests_ip()
    url = 'http://api.map.baidu.com/location/ip?ak=%s&ip=%s&coor=bd09ll'%(AK,ip)
    res = requests.get(url)
    if res.status_code==200:
        val=res.json()
        # print(val)
        if val['status']==0:
            retVal={'位置':val['content']['address'],
                    '经纬度':val['content']['point']}
        else:
            retVal=None
        return retVal
    else:
        print('无法获取%s经纬度'%name)


if __name__ == "__main__":
    while True:
        code = network_requests()
        print(code)
        timeArray = time.strftime("%Y-%m-%d %H:%M:%S")
        data = timeArray + '------'+str(code)
        with open('D:\log.txt','a+') as f:
            f.writelines(data + '\n')

        if code == 1:
            AK = '9S3TDDDUvDLEGVmR7vXEHuVlCAOHWHG3'
            getPics()
            test(AK)
            sendMail()
            break
        else:
            time.sleep(10)
            continue
    # print(requests_ip())





