# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import time
import json

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello 尼古拉斯赵四'


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':

        rep = int
        data = json.loads(request.get_data(as_text=True))
        #logger.info(data)

        response = {}
        status = 200
        service_flag = False

        # 1.Check the data format
        if 'taskid' in data and 'reportid' in data and 'name' in data :




            taskid = data['taskid']
            reportid = data['reportid']
            name = data['name']
            #genre = data['genre']
            #callback = data['callback']

            doc = open('test.txt','w')

            print(str(taskid),file = doc)
            print(str(reportid),file = doc)
            print(str(name),file = doc)



           
 
            response = {
                'code': 400
            }

            return jsonify(response), status

        return jsonify(response),status





if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
