# -*- coding: utf-8 -*-

from tasks.celery_config import celery
from celery.result import AsyncResult
from services.logger_service import LogService
from services.download_service import DownloadService
import os, requests

BACKEND_HOST = 'localhost:5000'
BACKEND_NOTIFY_URL = 'http://' + BACKEND_HOST + '/api/notify/surfaceImage'

@celery.task
def surface_image(id_, image_path):
    # 1. Run the algorithm
    level, cornealArea, damagedArea = surface_example(image_path)

    # 2. Save status and result to database

    # 3. Notify the backend
    request_body = {
        'id': id_,
        'level': level,
        'cornealArea': cornealArea,
        'damagedArea': damagedArea
    }

    res = requests.post(url=BACKEND_NOTIFY_URL, json=request_body, headers={'Content-Type': 'application/json;charset=utf-8'})
    print(res.text)
    print(res)


    return id_, level, cornealArea, damagedArea

def surface_example(image_path):
    level = 1
    cornealArea = 1.0
    damagedArea = 1.0
    return level, cornealArea, damagedArea

'''notify example
{
    'id': 1,
    'level': 1,
    'cornealArea': 1.0,
    'damagedArea': 1.0,
}
'''