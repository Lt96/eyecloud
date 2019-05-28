#coding=utf-8
import requests, json

data = {
    'taskid' : 11,
    'reportid'  : 23,
    'name' : '潇洒'
}

headers = {'Content-type': 'multipart/form-data'}

files = {'file123': open('./016.jpg', 'rb')}

#r = requests.post('http://172.18.8.139:5000/upload', files=files, data=data, headers=headers)
#r = requests.post('http://172.18.8.139:5000/upload', files=files)
r = requests.post('http://172.18.8.139:5000/upload', data=json.dumps(data), headers=headers)
