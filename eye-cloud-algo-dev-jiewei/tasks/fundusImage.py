# -*- coding: utf-8 -*-

from tasks.celery_config import celery
from celery.result import AsyncResult
import os, json
from services.logger_service import LogService
from services.download_service import DownloadService
from algorithms.dr.classify import DRDectect
import tensorflow as tf
import numpy as np
import requests

logger = LogService()
download_service = DownloadService()

filePath = "2018/8/26/c0de15f2b75f5f8098349299867b2ea9-1535291315852.jpeg"
DOWNLOAD_PATH = './download'
BACKEND_HOST = 'localhost:5000'
BACKEND_NOTIFY_URL = 'http://' + BACKEND_HOST + '/api/notify/fundusImage'
CONFIG_PATH = './algorithms/config.json'

with open(CONFIG_PATH, 'r') as config_file:
    CONFIG = json.load(config_file)
    # initial
    with tf.variable_scope('', reuse=tf.AUTO_REUSE):
        dr_detection = DRDectect(CONFIG['dr'])
        dr_detection.initial()

@celery.task
def dr_classify(id_, images_path):
    # 1. Run the algorithm
    results = []
    for index in range(0, len(images_path)):
        image_path = images_path[index]
        store_path = download_service.download_file_from_oss(image_path)
        print(store_path)
        # logger.info("Starting diabetes classfication algorithm")
        type_, probability, direction = dr_detection.classify(store_path)
        print(type_)
        result =  {
            'type': type_,
            'probability': np.asscalar(probability),
            'direction': direction
        }
        results.append(result)
        os.remove(store_path)

    # 2. Save status and result to database


    # 3. Notify the backend
    request_body = {
        'id': id_,
        'results': results
    }

    res = requests.post(url=BACKEND_NOTIFY_URL, json=request_body, headers={'Content-Type': 'application/json;charset=utf-8'})
    print(res.text)
    print(res)

    return id_, type_, probability, direction

def test_dr_classify(image_path):
    result = dr_classify.delay(image_path)
    taskid = result.id
    # print(taskid)
    # print(result.get(timeout=5))
    print(AsyncResult(taskid).get())


# test_diabates_classify(filePath)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime):                                 
            return obj.__str__()
        else:
            return super(MyEncoder, self).default(obj)


'''notify example
{
    'id': 1,
    'results':[{
        'type': '正常',
        'probabelity': 0.99999,
        'direction': '右眼'
    }]
}
'''