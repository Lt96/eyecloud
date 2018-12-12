# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, jsonify, Blueprint
from services.logger_service import LogService
from services.download_service import DownloadService

logger = LogService()
status_api = Blueprint('status', __name__)

@status_api.route('/fundusImage', methods=['POST'])
def getFundusImageStatus():
    data = request.get_json()
    logger.info(data)
    response_body = {}

    if not 'id' in data:
        id = data['id']
        response_body = {
            'code': 10001,
            'error': 'no task id'
        }

    # Get algorithm status from database
    '''
    response_body = {
        'code': 10002,
        'error': 'no task'
    }
    '''
    '''
    response_body = { # pending
        'code': 0,
        'status': 0
    }'''
    '''
    response_body = { # finished
        'code': 0,
        'status': 1,
        'results': [{
            'type': type_,
            'probability': probability,
            'direction': direction
        }]
    }'''

    return jsonify(response_body)

@status_api.route('/surfaceImage', methods=['POST'])
def getSurfaceImageStatus():
    data = request.get_json()
    logger.info(data)
    response_body = {}

    if not 'id' in data:
        id = data['id']
        response_body = {
            'code': 10001,
            'error': 'no task id'
        }

    # Get algorithm status from database
    '''
    response_body = {
        'code': 10002,
        'error': 'no task'
    }
    '''
    '''
    response_body = { # pending
        'code': 0,
        'status': 0
    }'''
    '''
    response_body = { # finished
        'code': 0,
        'status': 1,
        'result': {
            'level': level,
            'cornealArea': cornealArea,
            'demagedArea': demagedArea
        }
    }'''

    return jsonify(response_body)