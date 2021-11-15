# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import requests
import json


def get_cookie(IP):
    

    n = 1
    while n < 10:
        n+=1
        
        sid = get_login(IP)
        # print(sid)
        if sid ==1:
            time.sleep(2)
            continue
            
            
        else:
            # print(sid)
            return sid
            break
    

def get_login(IP):
    browser = webdriver.Chrome()
    
    browser.get('http://%s'%IP)

    print(123456789)

    try:
        if IP == "10.0.0.253":
            username = "admin"
            password = "password"
        if IP == "192.168.250.251":
            username = "admin"
            password = "password"
        if IP == "10.255.255.201":
            username = "admin"
            password = "password"
        browser.find_element_by_xpath('//*[@id="username"]').send_keys(username)
        # time.sleep(2)
        # exit(0)
        browser.find_element_by_xpath("//*[@id='password']").send_keys(password)
        # browser.send_keys(Keys.ENTER)//*[@id="username"]
        time.sleep(2)
        browser.find_element_by_xpath("//*[@id='login']").send_keys(Keys.ENTER)
    
            
        # print(source1)
        # exit(0)
        time.sleep(2)
        source = browser.page_source
        browser_get_Cookies  = browser.get_cookies()
        # print(type(browser_get_Cookies))
        print(browser_get_Cookies)
        #STU and office
        sid = browser_get_Cookies[3].get('value')

        #longshan
        if IP == "10.0.0.253":
            sid = browser_get_Cookies[4].get('value')
        # print("456789")
        print(sid)

        time.sleep(5)
        # ×Ô¶¯ÍË³öä¯ÀÀÆ÷
        browser.quit()
        return sid
    except:
        time.sleep(5)
        browser.quit()
        sid = 1
        return sid


def get_list(sid,IP,user_num,num):

    
    url = "http://%s/web/init.cgi/ac.dashboard.ap_list/getApList"%IP

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "Referer": "http://%s/ac/dashboard/ap-list.htm"%IP,
        "Origin": "http://%s"%IP,
        "Cookie": "LOCAL_LANG_COOKIE=zh; UI_LOCAL_COOKIE=zh; SID=%s; login=1; mac=c0b8.e647.5ca9; oid=1.3.6.1.4.1.4881.1.3.1.1.221; main_ui_cookie=dash_ap_list"%sid

    }

    data = {
        'Start': 1,
        'End': 10
    }

    if num == 1:
        data = {
            "Start": "1",
            "End": '10',
            "isLayerCenter": "false"
        }
    if num == 0:
        data = {
            "Start": "1",
            "End":user_num,
            "isLayerCenter": "false"
        }

    response = requests.post(url=url,headers=headers,data=data)
    JsonStr = json.dumps(response.json(), ensure_ascii=False) 
    users_list = json.loads(JsonStr)
    return users_list


def get_mac_list(IP,filename):
    sid = get_cookie(IP)
    print(sid)
    # exit(0)
    user_num = 1
    # print(response.text)
    user_list = get_list(sid,IP,user_num=1,num=1)
    user_num = user_list['data']['totalCount']
    user_list = get_list(sid,IP,user_num,num=0)


    # f = open(filename,'w+')
    with open(filename,'w+',encoding="utf-8") as f:
        for i in range(user_num):

            apgroup = user_list['data']['list'][i]['apgroup']
            apname = user_list['data']['list'][i]['apname']
            mac = user_list['data']['list'][i]['mac']
            print(apgroup,apname,mac)
            if "kejilou" in apname:
                continue
            a = "ap-config %s \n ap-mac %s \n ap-group %s\n\n"%(apname,mac,apgroup)
            f.write(a)
            # b=print(ap-config %s\
            # ap-mac %s\
            # ap-group %s)
    # f.close()


if __name__ == '__main__':
    IP_list = ['192.168.250.251','10.255.255.201','10.0.0.253']
    for IP in IP_list:
        filename = 'D://AP_%s.txt'%IP
        get_mac_list(IP,filename)
    

    
































"""
ap-config 10-101
 ap-mac c470.ab56.f948
 ap-group stdu_10
!
ap-config 10-102
 ap-mac c470.ab56.e004
 ap-group stdu_10
!
ap-config 10-103
 ap-mac c470.ab56.f64e
 ap-group stdu_10
!
ap-config 10-104
 ap-mac c470.ab56.f630
 ap-group stdu_10
"""








