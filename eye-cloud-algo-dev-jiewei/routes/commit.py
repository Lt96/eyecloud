# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, jsonify, Blueprint
from services.logger_service import LogService
from services.download_service import DownloadService
import urllib, os, json
import traceback
import tasks.fundusImage as fundusImage
import tasks.surfaceImage as surfaceImage

commit_api = Blueprint('commit', __name__)

logger = LogService()
download_service = DownloadService()

@commit_api.route('/commit', methods=['POST'])
def commit_image():
    data = request.get_json()
    logger.info(data)

    response = {}
    status = 200
    service_flag = False

    # 1.Check the data format
    if 'id' in data and ('image' in data or 'images' in data):
        if isinstance(data['id'], int):
            service_flag = True

    if not service_flag:
        response = {
            'code': 10002
        }
        return jsonify(response), status

    # 2. Run the algorithms and insert status to database
    try:
        # surfaceImage algorithm
        if 'image' in data:
            id_ = data['id']
            image = data['image']
            # insert status to database

            # add task to the queue
            surfaceImage.surface_image.delay(id_, image)

        # fundusImage algorithm
        else:
            id_ = data['id']
            images = data['images']
                 
            # insert status to database

            # add task to the queue
            fundusImage.dr_classify.delay(id_, images)

        response = {
            'code': 0
        }

    except Exception as err:
        response = {
            'code': 10002
        }
        status = 500
        logger.info(traceback.format_exc())

    return jsonify(response), status