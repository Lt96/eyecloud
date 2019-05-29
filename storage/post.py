#coding=utf-8
import requests, json

url = 'http://172.18.8.139:5000/upload'

url2= 'http://172.18.8.142:22222/api/commit/fundusImage'

url3= 'http://172.18.8.142:22222/api/commit/mobilefundus'

data = {
    'taskid' : 31233,
    'reportid'  : 3231,
    'name' : '洒',
    'callback' : 'www.baidu.com'
}

json1 = {
"id": 759,
"images":["left.46.jpg"],
"genre":1,
"callback":"https://www.baidu.com"

}

#headers = {'Content-type': 'application/json'}

headers = {
    'Content-Type': "application/json",

    }

files = {'file': open('./3.pdf', 'rb')}

#r = requests.post('http://172.18.8.139:5000/upload', files=files, data=data, headers=headers)
#r = requests.post('http://172.18.8.139:5000/upload', files=files)
#r = requests.post(url2, data=json.dumps(json1),headers=headers)
#r = requests.post(url, json = json.dumps(json1) )
#r= requests.post(url, data = data, files = files)
r = requests.post(url3, data=data, headers=headers)

print (r.text)
