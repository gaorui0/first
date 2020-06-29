import requests


url = 'http://m.5c.com.cn/api/send/?'

data = {
    'apikey':'8150b1c3ac3be70923f39374d37b0cd7',
    'username':'tddx',
    'password':'asdf1234',
    'mobile':'18034534001', #手机号
    'content':'test it' #消息内容



}
client=requests.post(url=url,data=data)

print(client.text)
