# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, jsonify, Blueprint
from services.logger_service import LogService
from services.download_service import DownloadService
import urllib, os, json
import traceback
import tasks.fundusImage as fundusImage
import tasks.surfaceImage as surfaceImage
import tasks.mobilefundus as mobilefundus
from services.beforepro import pyc
from werkzeug.utils import secure_filename
import os, time

commit_api = Blueprint('commit', __name__)

logger = LogService()
download_service = DownloadService()



@commit_api.route('/commit/mobilefundus', methods=['POST'])
def commit_mobilefundus():
    
    data = request.form.to_dict()
    logger.info(data)
    taskid = str(data['taskid'])
    reportid = str(data['reportid'])
    name = str(data['name'])
    callback = str(data ['callback'])

    #doc = open('test.txt', 'w')

    #print(str(taskid), file=doc)
    #print(str(reportid), file=doc)
    #print(str(name), file=doc)

    try:
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print('localtime=' + localtime)
        # 系统当前时间年份
        year = time.strftime('%Y', time.localtime(time.time()))
        # 月份
        month = time.strftime('%m', time.localtime(time.time()))
        # 日期
        day = time.strftime('%d', time.localtime(time.time()))
        # 具体时间 小时分钟毫秒
        hms = time.strftime('%H%M%S', time.localtime(time.time()))
        filePathPrefix = '/root/data/yuanz'
        fileYear = filePathPrefix + '/' + year
        fileMonth = fileYear + '/' + month
        fileDay = fileMonth + '/' + day
        fileSecond = fileDay + '/' + hms
        if not os.path.exists(fileYear):
            os.mkdir(fileYear)
            os.mkdir(fileMonth)
            os.mkdir(fileDay)
            os.mkdir(fileSecond)
        else:
            if not os.path.exists(fileMonth):
                os.mkdir(fileMonth)
                os.mkdir(fileDay)
                os.mkdir(fileSecond)
            else:
                if not os.path.exists(fileDay):
                    os.mkdir(fileDay)
                    os.mkdir(fileSecond)
                else:
                    if not os.path.exists(fileSecond):
                        os.mkdir(fileSecond)
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, fileSecond,
                                   secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        mobilefundus.dr_classify.delay(taskid, reportid, name, upload_path, callback)
    except Exception as err:
        print(err)
    status = 200

    response = {
        'code': 400
    }

    return jsonify(response), status




@commit_api.route('/commit/surfaceImage', methods=['POST'])
def commit_surfaceImage():
    rep=int
    data = request.get_json()
    logger.info(data)

    response = {}
    status = 200
    service_flag = False

    # 1.Check the data format
    if 'id' in data and 'images' in data and 'genre' in data and 'callback' in data:
        if isinstance(data['id'], int):
            service_flag = True

    if not service_flag:

        response = {
            'code': 100021
        }
        return jsonify(response), status
    id_ = data['id']
    images = data['images']
    image = images[0]
    genre = data['genre']
    callback=data['callback']

    try:
        if genre ==2:
            connect = pyc()
            rep= connect.pytomy(id_, '0', genre,rep)

            if rep == 0:
                response = {
                    'code': 100022
                }

                return jsonify(response), status
            else:
            # add task to the queue
                surfaceImage.surface_image.delay(id_, image,callback)
                response = {
                'code': 2
                }
                return jsonify(response), status



        else:
            response = {
            'code': 100023
            }

            return jsonify(response), status



    except Exception as err:
        response = {
            'code': 100024
        }
        status = 500
        logger.info(traceback.format_exc())

    return jsonify(response), status




@commit_api.route('/commit/fundusImage', methods=['POST'])
def commit_fundusImage():
    rep=int
    data = request.get_json()
    logger.info(data)

    response = {}
    status = 200
    service_flag = False

    # 1.Check the data format
    if 'id' in data and 'images' in data and 'genre' in data and 'callback' in data:
        if isinstance(data['id'], int):
            service_flag = True

    if not service_flag:
        response = {
            'code': 100021
        }
        return jsonify(response), status

    id_ = data['id']
    image = data['images']

    genre = data['genre']
    callback=data['callback']

    try:
        if genre == 1:
            connect = pyc()
            rep= connect.pytomy(id_, '0', genre,rep)

            if rep == 0:
                response = {
                    'code': 100022
                }
                return jsonify(response), status
            else:
                # add task to the queue
                fundusImage.dr_classify.delay(id_, image, callback)
                response = {
                'code': 1
                }
                return jsonify(response), status



        else:
            response = {
                'code': 100023
            }
            return jsonify(response), status



    except Exception as err:
        response = {
            'code': 100024
        }
        status = 500
        logger.info(traceback.format_exc())


    return jsonify(response), status
